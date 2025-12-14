from decimal import Decimal
from app.repositories.transaction_repo import TransactionRepo
from app.repositories.user_repo import UserRepo
from app.services.currency_service import CurrencyService

class BalanceService:
    def __init__(self, user_repo: UserRepo, tx_repo: TransactionRepo, service: CurrencyService):
        self.user_repo = user_repo
        self.tx_repo = tx_repo
        self.service = service

    def check_and_calculate_balance(self, user_id: str, amount: Decimal, currency: str, transaction_type: str) -> Decimal:
        user = self.user_repo.get_by_id(user_id=user_id)
        if user is None:
            raise ValueError("User not found")
        
        amount_myr = self.service.to_myr(amount=amount, currency=currency)
        wallet_balance = user.wallet_balance

        pending_total = self.tx_repo.sum_pending_purchases_myr(user_id=user_id)
        available_balance = wallet_balance - pending_total
        
        if transaction_type in {"purchase", "withdrawal"}:
            if amount_myr <= 0:
                raise ValueError("Amount must be positive")
            
            if amount_myr > available_balance:
                raise ValueError("Insufficient available balance")
            
            new_balance = wallet_balance - pending_total
        
        elif transaction_type in {"refund"}:
            new_balance = wallet_balance + abs(available_balance)

        elif transaction_type in {"topup"}:
            if amount_myr <= 0:
                raise ValueError("Top-up amount must be positive")
            
            new_balance = wallet_balance + amount_myr

        else:
            raise ValueError("Unsupported transaction type")
        
        if new_balance < Decimal("0.00"):
            raise ValueError("Balance must not go negative")

        return new_balance
    
    def update_balance(self, user_id: str, new_balance: Decimal):
        user = self.user_repo.update_balance(user_id=user_id, new_balance=new_balance)
        user.wallet_balance = new_balance

        return user