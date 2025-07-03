from aiogram import types
from aiogram import Dispatcher
from aiogram.filters import Command

from database.db import get_user_history

# Обработчик команды /history
async def history_command(message: types.Message):
    user_id = str(message.from_user.id)
    history = await get_user_history(user_id)
    if history:
        response = "Ваша история запросов:\n"
        for entry in history:
            response += f"{entry.timestamp}: {entry.query_type} {entry.currency} - {entry.rate}\n"
        await message.answer(response)
    else:
        await message.answer("История запросов пуста.")

# Регистрация обработчика
def register_handlers_history(dp: Dispatcher):
    dp.message.register(history_command, Command('history'))