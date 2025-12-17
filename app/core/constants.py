from decimal import Decimal

VALID_TRANSACTIONS = {
    "pending": {"completed", "failed"},
    "completed": {"reversed"},
    "failed": set(),
    "reversed": set(),
}

FX_RATES = {
    "MYR": Decimal("1.0"),
    "USD": Decimal("4.70"),
    "SGD": Decimal("3.45"),
}

MIN_AMOUNT = Decimal("0.01")
MAX_AMOUNT = Decimal("50000")

POSITIVE_TYPES = {"topup", "refund"}
NEGATIVE_TYPES = {"purchase", "withdrawal"}
