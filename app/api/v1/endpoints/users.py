from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.db.base import get_db
from app.repositories.user_repo import UserRepo
from app.schemas.user import CreateUserRequest, ResponseUserRequest
from app.services.user_service import UserService

router = APIRouter(prefix="/user", tags=["users"])

@router.post("/create")
def create_user(payload: CreateUserRequest, db: Session = Depends(get_db)):
    repo = UserRepo(db=db)
    service = UserService(repo=repo, db=db)

    try:
        user = service.create_user(email=payload.email, full_name=payload.full_name, currency=payload.currency)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"user_id": user.user_id, "message": "User created"})
    
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@router.get("/{user_id}", response_model=ResponseUserRequest)
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    repo = UserRepo(db=db)
    service = UserService(repo=repo, db=db)

    user = service.get_by_id(user_id=user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
        
    return user
    