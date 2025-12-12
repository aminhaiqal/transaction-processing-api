import uuid
import datetime
from sqlalchemy import Column, String
from decimal import Decimal
from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    user_id=Column(String, primary_key=True, default=lambda: str(uuid.uuid4))
    email=Column(String, unique=True, nullable=False)
    full_name=Column(String, nullable=False)
    wallet_balance=Column(Decimal, nullable=False, default=0.00)
    currency=Column(String, nullable=False, default="MYR")
    status=Column(String, nullable=False, default="active")
    