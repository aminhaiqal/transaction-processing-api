from sqlalchemy import func
from sqlalchemy.orm import Session
from decimal import Decimal
from app.models.transaction import Transaction


class TransactionRepo:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, transaction_id: str):
        return self.db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    
    def create(self, **kwargs):
        tx = Transaction(**kwargs)
        self.db.add(tx)
        return tx
    
    def list_by_user(self, user_id: str):
        return self.db.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    def sum_pending_purchases_myr(self, user_id: str) -> Decimal:
        return (
            self.db.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
                Transaction.user_id == user_id,
                Transaction.status == "pending",
                Transaction.transaction_type == "purchase",
            ).scalar()
        )