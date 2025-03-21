import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.token import TokenValidationError
from avito_parser import AvitoParser
from loadenv import envi

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
try:
    bot = Bot(token=envi.token)
    dp = Dispatcher()
except TokenValidationError:
    logging.error("Неверный токен бота. Проверьте переменную окружения TOKEN.")
    exit(1)

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Отправь мне URL объявления с Avito, и я покажу тебе информацию о нём.")

# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: Message):
    url = message.text
    if "avito.ru" in url:
        await message.answer("Обрабатываю запрос...")
        parser = AvitoParser()
        try:
            parser.parse(url)
            response = (
                f"📍 {parser.full_address}\n"
                f"💵 {parser.price_value}₽\n\n"
                f"🚪 {parser.rooms}комн.\n"
                f"📐 {parser.total_area}м²\n"
                f"🪜 {parser.floor}"
            )
            await message.answer(response)
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
 #       finally:
 #           parser.close()
    else:
        await message.answer("Пожалуйста, отправьте корректный URL объявления с Avito.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())