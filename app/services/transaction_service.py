from app.core.constants import VALID_TRANSACTIONS
from app.models.transaction import Transaction
from app.models.user import User
from app.repositories.transaction_repo import TransactionRepo
from app.services.balance_service import BalanceService
from app.validators.transaction_validator import TransactionValidator
from datetime import datetime, timedelta
from decimal import Decimal

class TransactionService:
    def __init__(self, repo: TransactionRepo, validator: TransactionValidator, service: BalanceService):
        self.repo = repo
        self.validator = validator
        self.service = service

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

    def purchase_process(self, user: User, amount: Decimal, currency: str, idempotency_key):
        transaction_type = "purchase"

        try:
            existing = self.is_duplicated(user_id=User.user_id, idempotency_key=idempotency_key)
            if existing:
                return existing
            
            self.validator.validate_transaction_amount(amount=amount, currency=currency, transaction_type=transaction_type)
            new_balance = self.service.check_and_calculate_balance(user_id=User.user_id, amount=amount, currency=currency, transaction_type=transaction_type)
            
            tx = self.repo.create(
                user_id=user.user_id,
                amount=amount,
                currency=currency,
                transaction_type=transaction_type,
                status="pending"
            )
            tx = self.update_status(tx=tx, new_status="completed")

            user.wallet_balance = self.service.update_balance(user_id=user.user_id, new_balance=new_balance)

            self.repo.db.commit()
            self.repo.db.refresh(tx)
            return tx
        
        except Exception:
            self.repo.db.rollback()