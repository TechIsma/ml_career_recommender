from typing import List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid
from abc import ABC, abstractmethod


class Profession(Enum):
    DEVELOPER = "Программист"
    TEACHER = "Учитель"
    DOCTOR = "Врач"
    UNKNOWN = "Не определено"


@dataclass
class Balance:
    _amount: float = 0.0

    def deposit(self, amount: float):
        self._amount += amount

    def withdraw(self, amount: float):
        if amount > self._amount:
            raise ValueError("Недостаточно средств")
        self._amount -= amount

    def get(self):
        return self._amount


@dataclass
class Transaction:
    timestamp: datetime
    amount: float
    type: str
    description: str

    def summary(self) -> str:
        return f"{self.timestamp} - {self.type}: {self.amount} ({self.description})"


@dataclass
class PredictionTask:
    id: str
    user_id: str
    skills: List[str]
    result: List[str]
    status: str
    timestamp: datetime

    def describe(self) -> str:
        return f"Task {self.id} for user {self.user_id} - status: {self.status}, result: {self.result}"


@dataclass
class User:
    id: str
    name: str
    balance: Balance = field(default_factory=Balance)
    transactions: List[Transaction] = field(default_factory=list)

    def add_transaction(self, amount: float, type: str, description: str):
        self.transactions.append(Transaction(datetime.now(), amount, type, description))

    def make_prediction(self, advisor, skills: List[str]) -> PredictionTask:
        result = advisor.advise(skills)
        return PredictionTask(id=str(uuid.uuid4()), user_id=self.id, skills=skills, result=result, status="Completed", timestamp=datetime.now())


@dataclass
class SkillSet:
    skills: List[str]

    def __str__(self):
        return ", ".join(self.skills)

    def add_skill(self, skill: str):
        self.skills.append(skill)

    def remove_skill(self, skill: str):
        if skill in self.skills:
            self.skills.remove(skill)


# Новый абстрактный класс для советников профессий
class ProfessionAdvisor(ABC):
    @abstractmethod
    def advise(self, skills: List[str]) -> List[str]:
        pass


class RuleBasedAdvisor(ProfessionAdvisor):
    def advise(self, skills: List[str]) -> List[str]:
        if "programming" in skills:
            return [Profession.DEVELOPER.value]
        elif "teaching" in skills:
            return [Profession.TEACHER.value]
        elif "biology" in skills:
            return [Profession.DOCTOR.value]
        else:
            return [Profession.UNKNOWN.value]


# Пример использования:
# advisor = RuleBasedAdvisor()
# user = User(id="1", name="Иван")
# skills = SkillSet(skills=["programming", "math"])
# prediction_task = user.make_prediction(advisor, skills.skills)
# print(prediction_task.describe())
