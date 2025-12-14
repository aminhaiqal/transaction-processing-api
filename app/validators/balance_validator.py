from decimal import Decimal
from app.repositories.transaction_repo import TransactionRepo
from app.services.balance_service import BalanceService


class BalanceValidator:
    def __init__(self, service: BalanceService, repo: TransactionRepo):
        self.service = service

    def validate_purchase_funds(self, available_balance: Decimal, purchase_amount_myr: Decimal):
        if purchase_amount_myr < Decimal("0.00"):
            raise ValueError("Purchase amount must be positive")
        
        if purchase_amount_myr > available_balance:
            raise ValueError("Insufficient available balance")
        