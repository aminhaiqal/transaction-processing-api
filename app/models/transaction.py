import uuid
from decimal import Decimal
from sqlalchemy import Column, Integer, String
from .base import Base, TimestampMixin


class Transaction(Base, TimestampMixin):
    __tablename__= "transactions"

    transaction_id=Column(String, primary_key=True, default=lambda: str(uuid.uuid4))
    user_id=Column(String, nullable=False)
    amount=Column(Decimal, nullable=False)
    currency=Column(String, nullable=False)
    merchant_name=Column(String, nullable=False)
    merchant_category=Column(String, nullable=False)
    transaction_type=Column(String, nullable=False)
    status=Column(String, nullable=False)
    fraud_score=Column(Integer, default=0)
    fraud_flags=Column(String)
    original_transaction_id=Column(String)
    metadata=Column(String)
