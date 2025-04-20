from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..src import schemas, crud
from ..src.database import SessionLocal
from ..src.auth import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me", response_model=schemas.User)
def read_user_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@router.get("/balance", response_model=float)
def get_balance(current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user.balance

@router.post("/balance/deposit")
def deposit_balance(amount: float, current_user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    updated_user = crud.update_user_balance(db, current_user.id, amount)
    crud.create_transaction(db, {
        "user_id": current_user.id,
        "amount": amount,
        "transaction_type": "deposit",
        "description": "Balance deposit"
    })
    return {"new_balance": updated_user.balance}