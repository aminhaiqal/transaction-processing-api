from decimal import Decimal

from app.core.constants import MIN_AMOUNT, MAX_AMOUNT, NEGATIVE_TYPES, POSITIVE_TYPES
from app.services.currency_service import CurrencyService

class TransactionValidator:
    def __init__(self, service: CurrencyService):
        self.service = service

    def validate_transaction_amount(self, amount: Decimal, currency: str, transaction_type: str):
        if abs(amount) < Decimal(str(MIN_AMOUNT)):
            raise ValueError("Amount must be greater than RM 0.01")
    
        amount_myr = abs(self.service.to_myr(amount, currency))
        if amount_myr > Decimal(str(MAX_AMOUNT)):
            raise ValueError("Amount must be lesser than RM 50,000")
        
        if transaction_type in POSITIVE_TYPES and amount <= 0:
            raise ValueError(f"{transaction_type} amount must be positive")
        
        if transaction_type in NEGATIVE_TYPES and amount >= 0:
            raise ValueError(f"{transaction_type} amount must be negative")
