# app/routers/telegram_bot.py

import telebot
from fastapi import APIRouter
from fastapi.responses import JSONResponse

TOKEN = "your-telegram-bot-token"  # мой токен
bot = telebot.TeleBot(TOKEN)

router = APIRouter()

# Функция для отправки сообщений в Telegram
def send_telegram_message(message: str, chat_id: str):
    bot.send_message(chat_id=chat_id, text=message)

# Роут для отправки сообщения через Telegram
@router.get("/send_telegram")
def send_message_to_telegram(message: str, chat_id: str):
    try:
        send_telegram_message(message, chat_id)
        return JSONResponse(content={"message": "Message sent successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
