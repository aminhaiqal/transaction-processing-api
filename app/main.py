from fastapi import FastAPI

from app.schemas.transaction import TransactionCreate, TransactionResponse

app = FastAPI()

@app.post("/transactions", response_model=TransactionResponse)
def create_transaction(data: TransactionCreate):
    return {
        "transaction_id": "txn-123",
        "user_id": data.user_id,
        "amount": data.amount,
        "status": "completed"
    }

# Run: uvicorn app.main:app --reload
# Test: curl -X POST http://localhost:8000/transactions -d '{"amount": 100}'