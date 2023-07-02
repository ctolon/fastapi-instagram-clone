from pydantic import BaseModel

class AuthLogin(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    