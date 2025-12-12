from sqlalchemy.orm import Session

from app.models.transaction import Transaction

class TransactionRepo:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, transaction_id: str):
        return self.db.query(Transaction).filter(Transaction.transaction_id == transaction_id).first()
    
    def create(self, **kwargs):
        tx = Transaction(**kwargs)
        self.db.add(tx)
        self.db.commit()
        self.db.refresh(tx)

        return tx
    
    def list_by_user(self, user_id: str):
        return self.db.query(Transaction).filter(Transaction.user_id == user_id).all()
    
    def update_status(self, transaction_id: str, status: str):
        tx = self.get_by_id(transaction_id=transaction_id)
        if tx:
            tx.status = status
            self.db.commit()
            self.db.refresh(tx)

        return tx