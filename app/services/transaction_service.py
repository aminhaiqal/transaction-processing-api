from sqlalchemy.orm import Session
from app.core.constants import VALID_TRANSACTIONS
from app.models.transaction import Transaction
from app.models.user import User
from app.repositories.transaction_repo import TransactionRepo
from app.services.balance_service import BalanceService
from app.services.user_service import UserService
from app.validators.transaction_validator import TransactionValidator
from datetime import datetime, timedelta
from decimal import Decimal

class TransactionService:
    def __init__(self, repo: TransactionRepo, validator: TransactionValidator, balance_service: BalanceService, user_service: UserService, db: Session):
        self.repo = repo
        self.db = db
        self.validator = validator
        self.balance_service = balance_service
        self.user_service = user_service

    def is_duplicated(self, user_id, idempotency_key):
        five_minutes_ago = datetime.now() - timedelta(minutes=5)

        return self.repo.db.query(Transaction).filter(
            Transaction.user_id == user_id,
            Transaction.idempotency_key == idempotency_key,
            Transaction.created_at >= five_minutes_ago
        ).first()

    def update_status(self, tx: Transaction, new_status):
        if new_status not in VALID_TRANSACTIONS[tx.status]:
            raise ValueError("Invalid status transition")
        
        tx.status = new_status
        return tx

    def transaction_process(self, user_id: str, amount: Decimal, currency: str, merchant_name: str, merchant_category: str, transaction_type: str, idempotency_key: str):
        user = self.user_service.get_by_id(user_id=user_id)

        try:
            existing = self.is_duplicated(user_id=user.user_id, idempotency_key=idempotency_key)
            if existing:
                return existing
            
            self.validator.validate_transaction_amount(amount=amount, currency=currency, transaction_type=transaction_type)
            new_balance = self.balance_service.check_and_calculate_balance(user=user, amount=amount, currency=currency, transaction_type=transaction_type)
            tx_data = {
                "user_id": user.user_id,
                "amount": amount,
                "currency": currency,
                "merchant_name": merchant_name,
                "merchant_category": merchant_category,
                "transaction_type": transaction_type,
                "status": "pending"
            }
            
            tx = self.repo.create(**tx_data)
            tx = self.update_status(tx=tx, new_status="completed")

            user.wallet_balance = self.balance_service.update_balance(user_id=user.user_id, new_balance=new_balance)

            self.db.commit()
            self.db.refresh(tx)
            self.db.refresh(user)
            return tx
        
        except Exception as e:
            self.db.rollback()