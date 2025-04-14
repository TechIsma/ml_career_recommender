import pika
import os

def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(
        os.getenv('RABBITMQ_DEFAULT_USER'),
        os.getenv('RABBITMQ_DEFAULT_PASS')
    )
    parameters = pika.ConnectionParameters(
        host='rabbitmq',
        port=5672,
        credentials=credentials,
        heartbeat=600
    )
    return pika.BlockingConnection(parameters)

def setup_queues():
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    
    # Очередь для ML задач
    channel.queue_declare(
        queue='ml_tasks',
        durable=True,
        arguments={'x-message-ttl': 86400000}  # TTL 24 часа
    )
    
    connection.close()