from .database import Base, engine, SessionLocal
from .models import User, Transaction, Prediction
from passlib.context import CryptContext
from datetime import datetime
import json

# Инициализация криптоконтекста для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    """Инициализация БД с гарантированным созданием демо-данных"""
    # Удаляем и создаем таблицы заново
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Создаем администратора с хешированным паролем
        admin = User(
            email="admin@example.com",
            username="admin",
            hashed_password=pwd_context.hash("admin123"),
            balance=1000.0,
            is_admin=True
        )
        db.add(admin)
        
        # Создаем демо-пользователя с хешированным паролем
        demo_user = User(
            email="user@example.com",
            username="demo_user",
            hashed_password=pwd_context.hash("demo123"),
            balance=500.0,
            is_admin=False
        )
        db.add(demo_user)
        
        db.flush()  # Получаем ID пользователей до commit
        
        # Создаем демо-транзакции
        transactions = [
            Transaction(
                user_id=admin.id,
                amount=1000.0,
                transaction_type="deposit",
                description="Initial admin deposit"
            ),
            Transaction(
                user_id=demo_user.id,
                amount=500.0,
                transaction_type="deposit",
                description="Initial user deposit"
            )
        ]
        db.add_all(transactions)
        
        # Создаем демо-предсказание
        prediction = Prediction(
            user_id=demo_user.id,
            input_data=json.dumps({
                "age": 25,
                "skills": ["Python", "SQL"],
                "experience": 3
            }),
            result=json.dumps({
                "career": "Data Scientist",
                "probability": 0.85
            }),
            confidence=0.85,
            cost=1.0,
            model_version="v1.0"
        )
        db.add(prediction)
        
        db.commit()
        
        # Проверка создания данных
        admin_check = db.query(User).filter(User.email == "admin@example.com").first()
        demo_check = db.query(User).filter(User.email == "user@example.com").first()
        transactions_check = db.query(Transaction).count()
        predictions_check = db.query(Prediction).count()
        
        if not admin_check or not demo_check:
            raise ValueError("Демо-пользователи не были созданы!")
        if transactions_check < 2:
            raise ValueError("Демо-транзакции не были созданы!")
        if predictions_check < 1:
            raise ValueError("Демо-предсказание не было создано!")
            
        print(f"Администратор создан: {admin_check.username}")
        print(f"Демо-пользователь создан: {demo_check.username}")
        print(f"Создано транзакций: {transactions_check}")
        print(f"Создано предсказаний: {predictions_check}")
            
    except Exception as e:
        db.rollback()
        print(f"Ошибка при инициализации БД: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    print("База данных успешно инициализирована с демо-данными")




