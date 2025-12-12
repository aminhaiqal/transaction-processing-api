import uuid
from sqlalchemy import Column, String, Numeric
from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    user_id=Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email=Column(String(255), unique=True, nullable=False)
    full_name=Column(String(255), nullable=False)
    wallet_balance=Column(Numeric(15,2), nullable=False, default=0.00)
    currency=Column(String(3), nullable=False, default="MYR")
    status=Column(String(20), nullable=False, default="active")
    