from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from decimal import Decimal

from app.services.transaction_service import TransactionService
from app.services.user_service import UserService

router = APIRouter(prefix="/transaction", tags=["transactions"])

@router.post("/purchase")
def create_purchase_transaction(user_id: str, amount: Decimal, currency: str, merchant_name: str, merchant_category: str, transaction_type: str, idempotency_key: str):
    if transaction_type != "purchase":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid transaction type")

    user_service = UserService()
    tx_service = TransactionService()

    user = user_service.get_by_id(user_id=user_id)
    existing = tx_service.is_duplicated(user_id=user_id, idempotency_key=idempotency_key)

    if existing:
        return existing
    
    transaction = tx_service.purchase_process(user=user, amount=amount, currency=currency, idempotency_key=idempotency_key)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"transaction": transaction, "message": "Purchase successful"})
