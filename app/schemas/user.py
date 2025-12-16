from pydantic import BaseModel
from decimal import Decimal

class CreateUserRequest(BaseModel):
    email: str
    full_name: str
    currency: str

class ResponseUserRequest(BaseModel):
    user_id: str
    email: str
    full_name: str
    wallet_balance: Decimal
    currency: str
    status: str

    class config:
        from_attribute = True