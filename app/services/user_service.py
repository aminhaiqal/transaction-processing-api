from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User
from app.repositories.user_repo import UserRepo


class UserService:
    def __init__(self, repo: UserRepo, db: Session):
        self.repo = repo
        self.db = db

    def get_by_id(self, user_id: str):
        user = self.repo.get_by_id(user_id=user_id)
        return user
    
    def create_user(self, email: str, full_name: str, currency: str) -> User:
        try:
            data = {
                "email": email,
                "full_name": full_name,
                "currency": currency,
            }
            user = self.repo.create(**data)
            self.db.commit()
            return user
        
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e