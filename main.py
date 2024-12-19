import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN, DADATA_TOKEN
from dadata import Dadata

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
dadata = Dadata(DADATA_TOKEN)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Функция для получения информации о Банке по его БИКу
def get_bic_info(bic_bank):
    try:
        result = dadata.find_by_id("bank", bic_bank)
        if not result:
            return "Информация по указанному БИК не найдена."

        bank_data = result[0]
        fields = {
            "Наименование": bank_data.get("value", "Нет данных"),
            "БИК": bank_data["data"].get("bic", "Нет данных"),
            "SWIFT": bank_data["data"].get("swift", "Нет данных"),
            "ИНН": bank_data["data"].get("inn", "Нет данных"),
            "КПП": bank_data["data"].get("kpp", "Нет данных"),
            "Регистрационный номер": bank_data["data"].get("registration_number", "Нет данных"),
            "Корреспондентский счет": bank_data["data"].get("correspondent_account", "Нет данных"),
            "Город для платежей": bank_data["data"].get("payment_city", "Нет данных"),
            "Тип кредитной организации": bank_data["data"]["opf"].get("type", "Нет данных"),
            "Адрес регистрации": bank_data["data"]["address"].get("value", "Нет данных"),
            "Дата регистрации": bank_data["data"]["state"].get("registration_date", "Нет данных"),
            "Статус организации": bank_data["data"]["state"].get("status", "Нет данных"),
        }

        info = "\n".join([f"{key}: {value}" for key, value in fields.items()])
        return info
    except Exception as e:
        logging.error(f"Ошибка при запросе к Dadata: {e}")
        return "Произошла ошибка при запросе информации. Попробуйте позже."

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Напиши мне БИК Банка, и я предоставлю информацию о нем.")

@dp.message()
async def get_bank_info(message: Message):
    bic = message.text.strip()
    if not bic.isdigit() or len(bic) != 9:
        await message.answer("Пожалуйста, введите корректный БИК (9 цифр).")
        return

    await message.answer("Ищу информацию, подождите...")
    bank_info = get_bic_info(bic)
    await message.answer(bank_info)

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
