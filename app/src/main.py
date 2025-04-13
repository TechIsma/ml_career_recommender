from .init_db import init_db
from .database import SessionLocal, Base, engine
from .crud import (
    create_user,
    get_user,
    update_user_balance,
    create_transaction,
    get_transactions,
    create_prediction,
    get_predictions
)
from .models import User, Prediction
from passlib.context import CryptContext
import json

# Инициализация для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_database_operations():
    # Полная очистка и инициализация БД
    Base.metadata.drop_all(bind=engine)
    init_db()
    
    db = SessionLocal()
    try:
        # 1. Проверка демо-пользователей
        print("\n1. Проверка демо-пользователей:")
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        demo_user = db.query(User).filter(User.email == "user@example.com").first()
        
        assert admin is not None, "Администратор не создан"
        assert demo_user is not None, "Демо-пользователь не создан"
        print(f"Администратор: {admin.username}, баланс: {admin.balance}")
        print(f"Демо-пользователь: {demo_user.username}, баланс: {demo_user.balance}")

        # 2. Тестирование пользователей
        print("\n2. Тестирование работы с пользователями:")
        test_user_data = {
            "email": "test@example.com",
            "username": "test_user",
            "password": pwd_context.hash("testpass123"),
            "is_admin": False
        }
        user = create_user(db, test_user_data)
        
        fetched_user = get_user(db, user.id)
        assert fetched_user.username == "test_user", "Ошибка получения пользователя"
        print(f"Пользователь создан: {fetched_user.username} (ID: {fetched_user.id})")

        # 3. Тестирование баланса и транзакций
        print("\n3. Тестирование операций с балансом:")
        updated_user = update_user_balance(db, user.id, 200.0)
        assert updated_user.balance == 200.0, "Ошибка пополнения баланса"
        
        updated_user = update_user_balance(db, user.id, -50.0)
        assert updated_user.balance == 150.0, "Ошибка списания средств"
        print(f"Текущий баланс: {updated_user.balance}")

        # 4. Тестирование транзакций
        print("\n4. Тестирование транзакций:")
        create_transaction(db, {
            "user_id": user.id,
            "amount": 200.0,
            "transaction_type": "deposit",
            "description": "Пополнение"
        })
        
        create_transaction(db, {
            "user_id": user.id,
            "amount": 50.0,
            "transaction_type": "withdrawal",
            "description": "Списание"
        })
        
        transactions = get_transactions(db, user.id)
        assert len(transactions) == 2, "Не все транзакции созданы"
        print("Транзакции:")
        for t in transactions:
            print(f"- {t.transaction_type}: {t.amount}")

        # 5. Тестирование предсказаний
        print("\n5. Тестирование предсказаний:")
        prediction_data = {
            "user_id": user.id,
            "input_data": json.dumps({"skills": ["Python"]}),
            "result": json.dumps({"career": "Data Scientist"}),
            "confidence": 0.85,
            "cost": 1.0
        }
        prediction = create_prediction(db, prediction_data)
        
        predictions = get_predictions(db, user.id)
        assert len(predictions) > 0, "Предсказания не созданы"
        print(f"Создано предсказаний: {len(predictions)}")
        print(f"Пример: {predictions[0].result}")

        # 6. Проверка связей
        print("\n6. Проверка связей между таблицами:")
        user_with_predictions = db.query(User).filter(User.id == user.id).first()
        assert user_with_predictions.predictions, "Связь User-Prediction не работает"
        print("Связи между таблицами работают корректно")

    except Exception as e:
        db.rollback()
        print(f"\nОшибка при тестировании: {e}")
        raise
    finally:
        db.close()
        print("\nТестирование завершено. Все проверки пройдены.")

if __name__ == "__main__":
    test_database_operations()