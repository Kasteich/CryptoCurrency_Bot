from aiogram import types
from aiogram import Dispatcher
from aiogram.filters import Command

from api.currency_api import get_currencies

# Обработчик команды /currencies
async def currencies_command(message: types.Message):
    currencies = get_currencies()
    if currencies:
        currencies_list = "Доступные валюты и их символы:\n"
        currencies_list += '\n'.join([f"{code} - {rate}" for code, rate in currencies.items()])
    else:
        currencies_list = "Не удалось загрузить список валют. Попробуйте позже."
    await message.answer(currencies_list)

# Регистрация обработчика
def register_handlers_currencies(dp: Dispatcher):
    dp.message.register(currencies_command, Command('currencies'))