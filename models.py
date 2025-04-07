from typing import List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid

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
