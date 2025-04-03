from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enum import Enum
from typing import List
import uuid
from datetime import datetime
import os

app = FastAPI(title="Career AI API")

# Модели данных (заменим dataclasses на Pydantic)
class Profession(str, Enum):
    DEVELOPER = "Программист"
    TEACHER = "Учитель"
    DOCTOR = "Врач"

class User(BaseModel):
    id: str
    name: str
    balance: float = 0.0

class PredictionRequest(BaseModel):
    user_id: str
    skills: List[str]

class PredictionResponse(BaseModel):
    user_id: str
    skills: List[str]
    result: List[Profession]
    cost: float
    timestamp: datetime

# Имитация базы данных
fake_db = {}

# Ваш существующий код с адаптацией
class CareerAI:
    def __init__(self):
        self.cost = 10.0
    
    def predict(self, skills: List[str]) -> List[Profession]:
        if "programming" in skills:
            return [Profession.DEVELOPER]
        return [Profession.TEACHER]

career_service = CareerAI()

# Роуты FastAPI
@app.post("/users/", response_model=User)
async def create_user(name: str):
    user_id = str(uuid.uuid4())
    fake_db[user_id] = User(id=user_id, name=name)
    return fake_db[user_id]

@app.post("/predict/", response_model=PredictionResponse)
async def make_prediction(request: PredictionRequest):
    user = fake_db.get(request.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.balance < career_service.cost:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    result = career_service.predict(request.skills)
    user.balance -= career_service.cost
    
    return PredictionResponse(
        user_id=user.id,
        skills=request.skills,
        result=result,
        cost=career_service.cost,
        timestamp=datetime.now()
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)