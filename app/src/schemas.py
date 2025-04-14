from pydantic import BaseModel
from datetime import datetime
from typing import Any

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    balance: float
    is_admin: bool
    

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
    
class PredictionBase(BaseModel):
    model_version: str
    input_data: dict[str, Any]
    result: dict[str, Any]
    confidence: float
    cost: float = 1.0

class PredictionCreate(PredictionBase):
    user_id: int

class Prediction(PredictionBase):
    id: int
    user_id: int
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str

class BalanceResponse(BaseModel):
    message: str
    new_balance: float

    class Config:
        orm_mode = True


