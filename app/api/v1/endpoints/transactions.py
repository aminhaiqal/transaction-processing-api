from fastapi import APIRouter
from decimal import Decimal

from app.services.transaction_service import TransactionService
from app.services.user_service import UserService

router = APIRouter(prefix="/transacitons", tags=["transactions"])

@router.post("/purchase")
def create_purchase_transaction(user_id: str, amount: Decimal, currency: str, idempotency_key: str):
    user_service = UserService()   
    tx_service = TransactionService()

    user = user_service.get_by_id(user_id=user_id)
    existing = tx_service.is_duplicated(user_id=user_id, idempotency_key=idempotency_key)

    if existing:
        return existing
    
    tx_service.purchase_process(user, amount, currency, idempotency_key)
