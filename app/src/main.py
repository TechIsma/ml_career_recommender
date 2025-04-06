from fastapi import FastAPI, HTTPException
from models import User, SkillSet
from services import CareerService, UserService

app = FastAPI()

@app.get("/")
def read_root():
    return {"message" : "Hello World"}
career_service = CareerService()
user_service = UserService(career_service)

@app.post("/register/")
def register_user(name: str):
    return user_service.register_user(name)

@app.post("/topup/")
def top_up_balance(user_id: str, amount: float):
    return user_service.top_up_balance(user_id, amount)

@app.post("/predict/")
def predict(user_id: str, skills: SkillSet):
    try:
        prediction = career_service.make_prediction(user_id, skills.skills)
        return {"result": prediction.result, "balance": prediction.remaining_balance}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))