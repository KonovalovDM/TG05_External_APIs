import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dadata import Dadata
from config import TOKEN, DADATA_TOKEN, DADATA_SECRET

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Инициализация Dadata
logging.basicConfig(level=logging.INFO)
dadata = Dadata(DADATA_TOKEN, DADATA_SECRET)

# Функция для стандартизации email
def clean_email(email):
    try:
        result = dadata.clean("email", email)
        if result:
            return {
                "Исходный email": result["source"],
                "Стандартизованный email": result["email"],
                "Локальная часть": result["local"],
                "Домен": result["domain"],
                "Тип": result["type"],
                "Код проверки": result["qc"],
            }
        else:
            return "Не удалось стандартизировать email. Проверьте введённые данные."
    except Exception as e:
        logging.error(f"Ошибка при запросе к Dadata: {e}")
        return "Произошла ошибка при обработке запроса. Попробуйте позже."

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Напиши мне email-адрес, и я проверю его корректность и стандартизирую.")

# Обработчик для стандартизации email
@dp.message()
async def handle_email(message: Message):
    email = message.text
    result = clean_email(email)
    if isinstance(result, dict):
        response = "\n".join([f"{key}: {value}" for key, value in result.items()])
    else:
        response = result

    await message.answer(response)

# Запуск бота
async def main():
    try:
        logging.info("Бот запущен!")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
