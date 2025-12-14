from fastapi import FastAPI
from app.models.base import Base
from app.db.base import engine
from app.api.v1.router import router as v1_router

app = FastAPI(title="Transaction Processing API")

@app.on_event("startup")
def startup():
    import app.models
    Base.metadata.create_all(bind=engine)

app.include_router(v1_router, prefix="/api")

# Run: uvicorn app.main:app --reload
