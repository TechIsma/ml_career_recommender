from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    balance: float
    is_admin: bool
    
    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    amount: float
    transaction_type: str
    description: str | None = None

class TransactionCreate(TransactionBase):
    user_id: int

class Transaction(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

