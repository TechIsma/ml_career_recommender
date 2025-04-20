from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..src import schemas, crud
from ..src.database import SessionLocal
from ..src.auth import get_current_user

router = APIRouter(prefix="predictions")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/predict", response_model=schemas.Prediction)
def make_prediction(
    input_data: dict,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Проверяем баланс
    if current_user.balance < 1.0:  # Предполагаем, что предсказание стоит 1.0
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    # Здесь должна быть логика вызова модели для предсказания
    # Пока используем заглушку
    prediction_result = {
        "career": "Data Scientist",
        "probability": 0.85
    }
    
    # Создаем запись о предсказании
    prediction = crud.create_prediction(db, {
        "user_id": current_user.id,
        "input_data": input_data,
        "result": prediction_result,
        "confidence": prediction_result.get("probability", 0.8),
        "cost": 1.0
    })
    
    # Обновляем баланс
    crud.update_user_balance(db, current_user.id, -1.0)
    
    return prediction

@router.get("/history", response_model=list[schemas.Prediction])
def get_prediction_history(
    skip: int = 0,
    limit: int = 100,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.get_predictions(db, current_user.id, skip=skip, limit=limit)