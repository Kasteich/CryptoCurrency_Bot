import logging
from aiogram import Bot
from aiogram.types import BotCommand
from handlers import register_handlers
from database.db import initialize_db
from loader import dp, bot

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка команд меню
async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запуск бота"),
        BotCommand(command="/help", description="Помощь"),
        BotCommand(command="/price", description="Курс валюты"),
        BotCommand(command="/low", description="Минимальный курс"),
        BotCommand(command="/high", description="Максимальный курс"),
        BotCommand(command="/convert", description="Конвертация валют"),
        BotCommand(command="/currencies", description="Список валют"),
        BotCommand(command="/crypto_currencies", description="Список криптовалют"),
        BotCommand(command="/history", description="История запросов")
    ]
    await bot.set_my_commands(commands)

# Настройка команд меню
async def on_startup():
    await set_bot_commands(bot)

# Инициализация базы данных
initialize_db()

# Регистрация обработчиков
register_handlers(dp)

# Запуск бота
async def main():
    await on_startup()
    try:
        logger.info("Запуск бота...")
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        logger.info("Бот был остановлен.")
    except KeyboardInterrupt:
        logger.info("Остановка бота по запросу пользователя.")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        logger.info("Закрытие хранилища FSM...")
        await dp.storage.close()

        logger.info("Закрытие сессии бота...")
        await bot.session.close()

        logger.info("Бот успешно завершил работу.")



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())