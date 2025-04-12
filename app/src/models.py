from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)  # Обязательное поле
    email = Column(String, unique=True, nullable=False)    # Обязательное поле
    hashed_password = Column(String, nullable=False)       # Обязательное поле
    balance = Column(Float, default=0.0)
    is_admin = Column(Boolean, default=False)

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    amount = Column(Float)
    transaction_type = Column(String)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
