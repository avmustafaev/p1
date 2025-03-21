import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties
from avito_parser import AvitoParser
from loadenv import envi

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера
bot = Bot(
    token=envi.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)  # Указываем parse_mode здесь
)
dp = Dispatcher()

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
                f"🪜 {parser.floor}\n\n"
                f'<a href="{url}">🔗 Переход на объявление</a>'
            )
            await message.answer(response, disable_web_page_preview=True)
        except Exception as e:
            logger.error(f"Ошибка при парсинге: {e}")
            await message.answer("Произошла ошибка при обработке запроса. Попробуйте ещё раз.")
    else:
        await message.answer("Пожалуйста, отправьте корректный URL объявления с Avito.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())