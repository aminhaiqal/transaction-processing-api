from decimal import Decimal
from app.core.constants import FX_RATES


class CurrencyService:
    def __init__(self):
        self.fx_rates = FX_RATES

    def to_myr(self, amount: Decimal, currency: str) -> Decimal:
        if currency not in self.fx_rates:
            raise ValueError("Unprocessed currency")
        
        rate = self.fx_rates[currency]
        if rate is None:
            raise ValueError(f"Unsupported currency: {currency}")
        
        return amount * rate