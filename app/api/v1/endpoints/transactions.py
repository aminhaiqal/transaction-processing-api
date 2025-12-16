from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.repositories.transaction_repo import TransactionRepo
from app.repositories.user_repo import UserRepo
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.balance_service import BalanceService
from app.services.currency_service import CurrencyService
from app.services.transaction_service import TransactionService
from app.services.user_service import UserService
from app.validators.transaction_validator import TransactionValidator

router = APIRouter(prefix="/transaction", tags=["transactions"])

@router.post("/", response_model=TransactionResponse)
def create_purchase_transaction(payload: TransactionCreate, idempotency_key: str = Header(..., alias="Idempotency-Key"), db: Session = Depends(get_db)):
    user_repo = UserRepo(db=db)
    transaction_repo = TransactionRepo(db=db)

    user_service = UserService(repo=user_repo, db=db)
    currency_service = CurrencyService()

    tx_service = TransactionService(
        repo=transaction_repo, 
        validator=TransactionValidator(service=currency_service),
        balance_service=BalanceService(user_repo=user_repo, tx_repo=transaction_repo, service=currency_service),
        user_service=user_service, 
        db=db
    )

    try:
        transaction = tx_service.transaction_process(
            user_id=payload.user_id, 
            amount=payload.amount,
            currency=payload.currency,
            merchant_name=payload.merchant_name,
            merchant_category=payload.merchant_category,
            transaction_type=payload.transaction_type,
            idempotency_key=idempotency_key
        )
        return transaction
    
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))