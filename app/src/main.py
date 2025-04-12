from .init_db import init_db
from .database import SessionLocal
from .crud import create_user, get_user, update_user_balance, create_transaction, get_transactions
from .models import User 

def test_database_operations():
    from .database import Base, engine
    Base.metadata.drop_all(bind=engine)
    init_db()  # Эта функция должна создавать демо-пользователей
    db = SessionLocal()
    try:
        # 0. Проверка демо-пользователей
        print("\n0. Проверка демо-пользователей:")
        
        # Сначала создаем демо-пользователей, если их нет
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin_data = {
                "email": "admin@example.com",
                "username": "admin",
                "password": "securepassword",
                "is_admin": True
            }
            admin = create_user(db, admin_data)
            print("Администратор создан")
        
        demo_user = db.query(User).filter(User.email == "user@example.com").first()
        if not demo_user:
            user_data = {
                "email": "user@example.com",
                "username": "demo_user",
                "password": "demopassword",
                "is_admin": False
            }
            demo_user = create_user(db, user_data)
            print("Демо-пользователь создан")
        
        print(f"Администратор: {admin.username}, баланс: {admin.balance}, is_admin: {admin.is_admin}")
        print(f"Демо-пользователь: {demo_user.username}, баланс: {demo_user.balance}")

        # 1. Тестирование создания нового пользователя
        print("\n1. Тестирование создания пользователя:")
        test_user = {
            "email": "test_user@example.com",
            "username": "test_user",
            "password": "testpass123"
        }
        
        created_user = create_user(db, test_user)
        print(f"Создан пользователь: {created_user.username} (ID: {created_user.id})")
        
        # 2. Тестирование получения пользователя
        print("\n2. Тестирование получения пользователя:")
        fetched_user = get_user(db, created_user.id)
        print(f"Получен пользователь: {fetched_user.username}, баланс: {fetched_user.balance}")
        
        # 3. Тестирование пополнения баланса
        print("\n3. Тестирование пополнения баланса:")
        updated_user = update_user_balance(db, created_user.id, 150.0)
        print(f"Баланс после пополнения: {updated_user.balance}")
        
        # Создаем транзакцию для пополнения
        deposit_transaction = {
            "user_id": created_user.id,
            "amount": 150.0,
            "transaction_type": "пополнение",
            "description": "Тестовое пополнение"
        }
        create_transaction(db, deposit_transaction)
        
        # 4. Тестирование списания средств
        print("\n4. Тестирование списания средств:")
        updated_user = update_user_balance(db, created_user.id, -50.0)
        print(f"Баланс после списания: {updated_user.balance}")
        
        # Создаем транзакцию для списания
        withdrawal_transaction = {
            "user_id": created_user.id,
            "amount": 50.0,
            "transaction_type": "списание",
            "description": "Тестовое списание"
        }
        create_transaction(db, withdrawal_transaction)
        
        # 5. Тестирование истории транзакций
        print("\n5. Тестирование истории транзакций:")
        transactions = get_transactions(db, created_user.id)
        print(f"Найдено {len(transactions)} транзакций:")
        for tx in transactions:
            print(f"- {tx.transaction_type}: {tx.amount} ({tx.description})")
        
    finally:
        db.close()
        print("\nТестирование завершено")

if __name__ == "__main__":
    test_database_operations()