from pydantic import BaseModel
from decimal import Decimal
import datetime

class TransactionCreate(BaseModel):
    user_id: str
    amount: Decimal
    currency: str
    merchant_name: str
    merchant_category: str
    transaction_type: str

class TransactionResponse(BaseModel):
    transaction_id: str
    user_id: str
    amount: Decimal
    currency: str
    merchant_name: str
    merchant_category: str
    transaction_type: str
    status: str
    created_at: datetime.datetime

    class Config:
        from_attribute: True

