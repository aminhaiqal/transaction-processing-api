import uuid
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Numeric, Index
from .base import Base, TimestampMixin


class Transaction(Base, TimestampMixin):
    __tablename__= "transactions"

    transaction_id=Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id=Column(String(36), ForeignKey("users.user_id"), nullable=False)
    amount=Column(Numeric(15,2), nullable=False)
    currency=Column(String(3), nullable=False)
    merchant_name=Column(String(255), nullable=False)
    merchant_category=Column(String(50), nullable=False)
    transaction_type=Column(String(20), nullable=False)
    status=Column(String(20), nullable=False)
    fraud_score=Column(Integer, default=0, nullable=False)
    fraud_flags=Column(Text)
    original_transaction_id=Column(String(36), ForeignKey("transactions.transaction_id"))
    metadata=Column(Text)

    __table_args__= (
        Index("idx_transaction_user_id", "user_id"),
        Index("idx_transaction_status", "status"),
        Index("idx_transaction_created_at", "created_at"),
        Index("idx_transactions_user_created", "user_id", "created_at"),
        Index("idx_transactions_fraud_score", "fraud_score")
    )
