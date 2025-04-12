from sqlalchemy.orm import Session
from . import models

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
