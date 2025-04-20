from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..src import schemas, crud
from ..src.auth import get_current_user
from ..src.database import get_db

router = APIRouter(
    prefix="/balance"
)

@router.post("/balance", response_model=schemas.BalanceResponse)
async def update_balance(
    amount: float,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if amount <= 0:
        raise HTTPException(
            status_code=400,
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