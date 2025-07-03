from aiogram import types
from aiogram import Dispatcher
from aiogram.filters import Command, CommandObject
from database.db import add_user
from handlers.convert import convert_command
from handlers.crypto_currencies import crypto_currencies_command
from handlers.currencies import currencies_command
from handlers.help import help_command
from handlers.history import history_command
from handlers.low_high import low_command, high_command
from handlers.price import price_command
from keyboards.ReplyKeyboardMarkup import get_main_keyboard


# Обработчик команды /start
async def start_command(message: types.Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username

    # Добавляем пользователя в БД
    user, created = add_user(user_id, username)

    if created:
       await message.answer(f"Привет, {username if username else 'Пользователь'}!\n"
                       f"Я - бот для отслеживания валют.\nИспользуй /help, "
                       f"чтобы узнать доступные команды.",
                       reply_markup=get_main_keyboard()
                            )
    else:
      await message.answer("Вы уже зарегистрированы! Используйте /help, чтобы узнать, что я умею.",
                           reply_markup=get_main_keyboard()
                           )

# Обработчик текстовых сообщений (для кнопок)
async def handle_text(message: types.Message):
    text = message.text.strip()
    if text == "/start":
        await start_command(message)
    elif text == "/help":
        await help_command(message)
    elif text == "/price":
        await price_command(message)
    elif text.startswith("/low"):
        await low_command(message)
    elif text.startswith("/high"):
        await high_command(message)
    elif text.startswith("/convert"):
        await convert_command(message)
    elif text == "/currencies":
        await currencies_command(message)
    elif text == "/crypto_currencies":
        await crypto_currencies_command(message)
    elif text == "/history":
        await history_command(message)
    else:
        await message.answer("Неизвестная команда. Используйте /help для списка команд.")

# Регистрация обработчика
def register_handlers_start(dp: Dispatcher):
    dp.message.register(start_command, Command('start'))
    dp.message.register(handle_text)

