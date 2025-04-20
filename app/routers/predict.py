from fastapi import APIRouter
from uuid import uuid4
from ml_service.rabbitmq import send_task_to_queue
from pydantic import BaseModel
from typing import Dict

router = APIRouter()

class PredictionRequest(BaseModel):
    user_id: int
    input_data: Dict

@router.post("/predict")
def predict_task(request: PredictionRequest):
    task = {
        "task_id": str(uuid4()),
        "user_id": request.user_id,
        "input_data": request.input_data
    }
    send_task_to_queue(task)
    return {"status": "Task sent", "task_id": task["task_id"]}
