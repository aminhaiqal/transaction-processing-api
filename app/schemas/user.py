from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    email: str
    full_name: str
    currency: str