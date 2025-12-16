from fastapi import APIRouter
from app.api.v1.endpoints import users, transactions

router = APIRouter(prefix="/v1")
router.include_router(users.router)
router.include_router(transactions.router)