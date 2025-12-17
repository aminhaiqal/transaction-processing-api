from app.enums.user_status import UserStatus
from app.models.user import User


class UserValidator:
    def __init__(self):
        pass

    def validate_can_transact(self, user: User):
        if user.status == UserStatus.CLOSED:
            raise ValueError("Account is closed")

        if user.status == UserStatus.SUSPENDED:
            raise ValueError("User is suspended")

        if user.status != UserStatus.ACTIVE:
            raise ValueError("User must be active")