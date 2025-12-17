from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepo:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id):
        return self.db.query(User).filter(User.user_id == user_id).first()

    def create(self, **kwargs):
        user = User(**kwargs)
        self.db.add(user)
        self.db.flush()
        return user
    
    def update_balance(self, user_id: str, new_balance: Decimal):
        user = (
            self.db.query(User)
            .filter(User.user_id == user_id)
            .with_for_update()
            .one()
        )

        user.wallet_balance = new_balance