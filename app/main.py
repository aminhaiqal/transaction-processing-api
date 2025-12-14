from fastapi import FastAPI
from app.models.base import Base
from app.db.base import engine

app = FastAPI()

@app.on_event("startup")
def startup():
    import app.models
    Base.metadata.create_all(bind=engine)

# Run: uvicorn app.main:app --reload
