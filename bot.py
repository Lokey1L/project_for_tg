import os
import logging
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram.utils.token import TokenValidationError
from openai import OpenAI
from dotenv import load_dotenv

# Загрузка переменных из .env
load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация OpenAI клиента
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Инициализация Telegram бота
try:
    bot = Bot(token=TELEGRAM_API_TOKEN)
except TokenValidationError:
    print("Неверный Telegram API токен.")
    exit()

dp = Dispatcher()
router = Router()
dp.include_router(router)

# Обработка команды /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я GPT-бот. Напиши мне любой вопрос.")

# Обработка текстовых сообщений
@router.message(F.text)
async def handle_question(message: Message):
    user_question = message.text

    try:
        chat_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_question}
            ]
        )
        answer = chat_response.choices[0].message.content
        await message.answer(answer, parse_mode=ParseMode.HTML)

    except Exception as e:
        logging.error(f"OpenAI Error: {e}")
        await message.answer("Произошла ошибка при обращении к OpenAI.")

# Запуск бота
if __name__ == '__main__':
    import asyncio
    asyncio.run(dp.start_polling(bot))
