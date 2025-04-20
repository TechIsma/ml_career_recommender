from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.src import auth
from app.src import crud
from app.src.schemas import Transaction

router = APIRouter(prefix="/transactions")

@router.get("/history", response_model=list[Transaction])
def get_transaction_history(
    db: Session = Depends(auth.get_db),
    current_user=Depends(auth.get_current_user),
    limit: int = 100
):
    return crud.get_transactions_by_user(db=db, user_id=current_user.id, limit=limit)