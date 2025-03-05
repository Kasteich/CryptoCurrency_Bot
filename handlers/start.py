from aiogram import types
from aiogram import Dispatcher
from database.db import add_user

# Обработчик команды /start
def start_command(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Добавляем пользователя в БД
    user, created = add_user(user_id, username)

    if created:
        message.answer(f"Привет, {username if username else 'Пользователь'}!"
                       f"\nЯ - бот для отслеживания валют.\nИспользуй /help, "
                       f"чтобы узнать доступные команды.")
    else:
        message.answer("Вы уже зарегистрированы! Используйте /help, чтобы узнать, что я умею.")

# Функция для регистрации хэндлера
def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_command, command=['start'])