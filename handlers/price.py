from aiogram import types
from aiogram.filters import Command
from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from api.currency_api import get_fiat_price, get_crypto_price
from database.db import add_query_history
from keyboards.InlineKeyboardMarkup import get_currency_keyboard
import logging

# Настройки логирования
logger = logging.getLogger(__name__)

# Обработчик команды /price
async def price_command(message: types.Message):
    args = message.text.split()[1:]
    if not args:
        await message.answer(
            "Выберите валюту:",
                reply_markup=get_currency_keyboard()
        )
        return

    symbol = args[0].upper()
    await handle_currency_price(message, symbol)

# Обработчик нажатий на inline-кнопки
async def handle_currency_callback(callback: CallbackQuery):
    if callback.data.startswith("currency_"):
        currency = callback.data.split("_")[1]
        await handle_currency_price(callback.message, currency)

# Общая функция для обработки валюты
async def handle_currency_price(message: types.Message, symbol: str):
    # Получаем данные для фиатных валют
    fiat_price = await get_fiat_price(symbol)
    if fiat_price:
        await message.answer(
            f"*Текущий курс {symbol}:* `{fiat_price} USD`",
            parse_mode="Markdown"
        )
        add_query_history(str(message.from_user.id), 'fiat', symbol, fiat_price)
        return

    # Получаем данные для криптовалют
    crypto_price = await get_crypto_price(symbol)
    if crypto_price:
        await message.answer(
            f"*Текущий курс {symbol}:* `{crypto_price} USD`",
            parse_mode="Markdown"
        )
        add_query_history(str(message.from_user.id), 'crypto', symbol, crypto_price)
    else:
        await message.answer(
            "*Валюта не найдена.* Проверьте символ валюты и попробуйте снова.",
            parse_mode="Markdown"
        )

# Регистрация обработчиков
def register_handlers_price(dp: Dispatcher):
    dp.message.register(price_command, Command('price'))
    dp.callback_query.register(handle_currency_callback)
