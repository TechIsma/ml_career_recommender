from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..src import schemas, crud
from ..src.database import SessionLocal
from ..src.auth import (
    get_current_user,
    create_access_token,
    authenticate_user,
    pwd_context
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/register",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED
)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = pwd_context.hash(user.password)
    return crud.create_user(db, {
        "email": user.email,
        "username": user.username,
        "hashed_password": hashed_password
    })

@router.post(
    "/token",
    response_model=schemas.Token
)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    print(f"Попытка входа для пользователя: {form_data.username}")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        print("Неверный логин или пароль")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    print(f" Токен создан: {access_token}")
    return {"access_token": access_token, "token_type": "bearer"}
@router.get(
    "/users/me",
    response_model=schemas.User
)
def read_user_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@router.get(
    "/users/balance",
    response_model=float
)
def get_user_balance(
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return current_user.balance

@router.post(
    "/balance/deposit",
    response_model=schemas.BalanceResponse
)
def deposit_to_balance(
    amount: float,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be positive"
        )
    
    updated_user = crud.update_user_balance(db, current_user.id, amount)
    crud.create_transaction(db, {
        "user_id": current_user.id,
        "amount": amount,
        "transaction_type": "deposit",
        "description": "Balance deposit"
    })
    
    return {
        "message": "Balance updated successfully",
        "new_balance": updated_user.balance
    }