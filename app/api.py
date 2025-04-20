from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, users, predictions, balance, transactions, telegram_bot
from app.src.database import SessionLocal, engine
from sqlalchemy.orm import Session
app = FastAPI(
    title="Career Recommendation API",
    description="API for career recommendations using LLM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
@app.get("/routes")
async def list_routes():
    return [
        {"path": route.path, "methods": route.methods}
        for route in app.routes
    ]
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        print("✅ Подключение к БД успешно")
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(balance.router)
app.include_router(predictions.router)
app.include_router(transactions.router)
app.include_router(telegram_bot.router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)