from app.repositories.user_repo import UserRepo


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def get_by_id(self, user_id: str):
        return self.repo.get_by_id(user_id=user_id)