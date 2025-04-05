# services.py
from models import User, PredictionTask
from typing import Dict
import uuid
from llm import get_profession_advice
from datetime import datetime


class BaseService:
    def __init__(self):
        self.users: Dict[str, User] = {}

    def get_user(self, user_id: str) -> User:
        user = self.users.get(user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        return user

class CareerService(BaseService):
    def make_prediction(self, user_id: str, skills: list[str]) -> PredictionTask:
        user = self.get_user(user_id)
        cost = 10.0
        user.balance.withdraw(cost)
        user.add_transaction(-cost, "withdraw", "Предсказание профессии")

        result = get_profession_advice(skills)
        task = PredictionTask(
            id=str(uuid.uuid4()),
            user_id=user_id,
            skills=skills,
            result=result,
            status="completed",
            timestamp=datetime.now()
        )
        return type("PredictionResult", (), {
            "result": result,
            "remaining_balance": user.balance.get()
        })

class UserService(BaseService):
    def __init__(self, career_service: CareerService):
        super().__init__()
        self.career_service = career_service

    def register_user(self, name: str) -> dict:
        user_id = str(uuid.uuid4())
        user = User(id=user_id, name=name)
        self.users[user_id] = user
        self.career_service.users = self.users  # shared
        return {"id": user_id, "name": name, "balance": 0.0}

    def top_up_balance(self, user_id: str, amount: float) -> dict:
        user = self.get_user(user_id)
        user.balance.deposit(amount)
        user.add_transaction(amount, "deposit", "Пополнение баланса")
        return {"id": user.id, "new_balance": user.balance.get()}
