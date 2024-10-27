from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str = None
    last_name: str = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    first_name: str = None
    last_name: str = None
    access_token: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserInfo(BaseModel):
    id: str
    email: EmailStr
    created_at: str
    first_name: str
    last_name: str = None
