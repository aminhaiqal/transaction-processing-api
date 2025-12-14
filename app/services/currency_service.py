from decimal import Decimal
from app.core.constants import FX_RATES


class CurrencyService:
    def __init__(self):
        self.fx_rates = FX_RATES

    def to_myr(self, amount: Decimal, currency: str) -> Decimal:
        if currency not in self.fx_rates[currency]:
            raise ValueError("Unprocessed currency")
        
        return amount * self.fx_rates[currency]