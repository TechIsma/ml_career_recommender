import os
import json
import pika
from ml_service.models import predict, MLInput
from app.src.database import SessionLocal
from app.src.models import Prediction

def save_prediction_to_db(user_id: int, input_data: dict, result: dict):
    """Сохранение результата предсказания в базу данных"""
    db = SessionLocal()
    try:
        prediction = Prediction(
            user_id=user_id,
            input_data=input_data,
            result=result,
            confidence=result.get('confidence', 0.0),
            cost=1.0,
            model_version="v1.0"
        )
        db.add(prediction)
        db.commit()
        db.refresh(prediction)
        return prediction
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def process_task(ch, method, properties, body):
    try:
        task = json.loads(body)
        
        # Валидация входных данных
        ml_input = MLInput(**task['input_data'])
        
        # Выполнение предсказания
        result = predict(task['input_data'])
        
        # Сохранение в БД
        save_prediction_to_db(
            user_id=task['user_id'],
            input_data=task['input_data'],
            result=result.dict()
        )
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Task processed: {task.get('task_id')}")
    except Exception as e:
        print(f"Error processing task: {str(e)}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def start_worker():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    
    channel.queue_declare(queue='ml_tasks', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='ml_tasks',
        on_message_callback=process_task
    )
    
    print(f"[Worker {os.getpid()}] Waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()