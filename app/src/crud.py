from . import models
from sqlalchemy.orm import Session
from .models import User, Transaction, Prediction
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_data: dict):
    """Создает пользователя с проверкой уникальности"""
    # Проверка существования пользователя
    if db.query(models.User).filter(models.User.username == user_data["username"]).first():
        raise ValueError(f"Имя пользователя {user_data['username']} уже занято")
    if db.query(models.User).filter(models.User.email == user_data["email"]).first():
        raise ValueError(f"Email {user_data['email']} уже зарегистрирован")
    
    db_user = models.User(
        email=user_data["email"],
        username=user_data["username"],
        hashed_password=user_data["password"] + "notreallyhashed"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user_balance(db: Session, user_id: int, amount: float):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.balance += amount
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def create_transaction(db: Session, transaction_data: dict):
    db_transaction = models.Transaction(**transaction_data)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, user_id: int):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()


def create_prediction(db: Session, prediction_data: dict):
    db_prediction = Prediction(**prediction_data)
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

def get_predictions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

def get_prediction_by_id(db: Session, prediction_id: int):
    """Получение конкретного предсказания по ID"""
    return db.query(Prediction).filter(Prediction.id == prediction_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return False
    return user