from pydantic import BaseModel
from decimal import Decimal

class TransactionCreate(BaseModel):
    user_id: str
    amount: Decimal
    currency: str
    merchant_name: str

class TransactionResponse(BaseModel):
    transaction_id: str
    user_id: str
    amount: Decimal
    status: str

