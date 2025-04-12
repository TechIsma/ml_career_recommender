from .database import Base, engine, SessionLocal
from .models import User

def init_db():
    """Инициализация БД с гарантированным созданием демо-данных"""
    # Удаляем и создаем таблицы заново
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # Используем одну сессию для всего процесса
    db = SessionLocal()
    try:
        # Создаем администратора
        admin = User(
            email="admin@example.com",
            username="admin",
            hashed_password="admin123",
            balance=1000.0,
            is_admin=True
        )
        db.add(admin)
        
        # Создаем демо-пользователя
        demo_user = User(
            email="user@example.com",
            username="demo_user",
            hashed_password="demo123",
            balance=500.0
        )
        db.add(demo_user)
        
        db.commit()  # Фиксируем изменения
        
        # Проверяем создание
        admin_check = db.query(User).filter(User.email == "admin@example.com").first()
        demo_check = db.query(User).filter(User.email == "user@example.com").first()
        
        if not admin_check or not demo_check:
            raise ValueError("Демо-пользователи не были созданы!")
            
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
if __name__ == "__main__":
    init_db()
    print("Database initialized with demo data")




