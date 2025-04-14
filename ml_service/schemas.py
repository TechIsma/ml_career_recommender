from pydantic import BaseModel

class MLTask(BaseModel):
    task_id: str
    user_id: int
    input_data: dict
    
    def validate(self):
        # Логика валидации
        return True