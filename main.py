from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
import uuid
from datetime import datetime

# 1. Перечисление профессий (просто варианты)
class Profession(Enum):
    DEVELOPER = "Программист"
    TEACHER = "Учитель"
    DOCTOR = "Врач"

# 2. Класс для хранения информации о пользователе
@dataclass
class User:
    id: str
    name: str
    balance: float = 0.0  # Начальный баланс 0
    
    def __post_init__(self):
        # При создании пользователя генерируем случайный ID
        self.id = str(uuid.uuid4())

# 3. Класс для хранения результатов предсказания
@dataclass
class Prediction:
    user_id: str
    skills: List[str]
    result: List[Profession]
    cost: float
    timestamp: datetime = datetime.now()

# 4. Простой "искусственный интеллект" для подбора профессий
class CareerAI:
    def __init__(self):
        self.cost = 10.0  # Стоимость одного предсказания
    
    def predict(self, skills: List[str]) -> List[Profession]:
        """Очень простая логика подбора профессий"""
        if "programming" in skills:
            return [Profession.DEVELOPER]
        return [Profession.TEACHER]

# 5. Основной сервис, который всё объединяет
class CareerService:
    def __init__(self):
        self.users: Dict[str, User] = {}  # Храним пользователей
        self.ai = CareerAI()  
    
    def register_user(self, name: str) -> User:
        """Регистрация нового пользователя"""
        user = User(id="", name=name)
        self.users[user.id] = user
        return user
    
    def make_prediction(self, user_id: str, skills: List[str]) -> Prediction:
        """Сделать предсказание профессии"""
        user = self.users.get(user_id)
        
        # Проверки
        if not user:
            raise ValueError("Пользователь не найден")
        if user.balance < self.ai.cost:
            raise ValueError("Недостаточно средств")
        
        # Делаем предсказание
        result = self.ai.predict(skills)
        
        # Создаем запись о предсказании
        prediction = Prediction(
            user_id=user.id,
            skills=skills,
            result=result,
            cost=self.ai.cost
        )
        
        # Списание средств
        user.balance -= self.ai.cost
        
        return prediction

# Пример использования
if __name__ == "__main__":
    main()
    service = CareerService()
    
    # 1. Регистрируем пользователя
    user = service.register_user("Алексей")
    print(f"Создан пользователь: {user.name}, ID: {user.id}")
    
    # 2. Пополняем баланс
    user.balance = 50.0
    print(f"Баланс: {user.balance} кредитов")
    
    # 3. Делаем предсказание
    try:
        prediction = service.make_prediction(user.id, ["programming"])
        print("\nРезультаты:")
        print(f"Навыки: {prediction.skills}")
        print(f"Рекомендации: {[p.value for p in prediction.result]}")
        print(f"Остаток баланса: {user.balance}")
    except ValueError as e:
        print(f"Ошибка: {e}")