from aiogram import types
from aiogram.filters import Command
from aiogram import Dispatcher
from api.currency_api import get_crypto_price_history, get_fiat_price_history
import logging

logger = logging.getLogger(__name__)

# Список поддерживаемых фиатных валют
FIAT_CURRENCIES = ['USD', 'RUB', 'EUR', 'GBP', 'JPY']


async def handle_price_command(message: types.Message, command_type: str):
    logger.info(f"Обрабатываем команду: {message.text}")
    args = message.text.strip().split()[1:]  # Получаем аргументы из команды
    logger.info(f"Аргументы команды: {args}")

    if not args:
        await message.answer(
            f"Пожалуйста, укажите символ валюты после команды. Например: /{command_type} BTC или /{command_type} USD")
        return

    symbol = args[0].upper()
    logger.info(f"Запрос курса для валюты: {symbol}")

    try:
        if symbol in FIAT_CURRENCIES:
            prices = await get_fiat_price_history(symbol)
            currency_type = "фиатной валюты"
        else:
            prices = await get_crypto_price_history(symbol)
            currency_type = "криптовалюты"

        logger.info(f"Цены для {symbol}: {prices}")

        if prices:
            price = min(prices) if command_type == 'low' else max(prices)
            message_text = f"{'Минимальный' if command_type == 'low' else 'Максимальный'} курс {symbol} за последние 7 дней: {price} USD"
            await message.answer(message_text)
        else:
            await message.answer(f"История цен для {symbol} не найдена.")
    except Exception as e:
        logger.error(f"Ошибка при получении данных для {symbol}: {e}")
        await message.answer(f"Ошибка при получении данных. Попробуйте позже.")


async def low_command(message: types.Message):
    logger.info(f"Получена команда /low с сообщением: {message.text}")
    await handle_price_command(message, 'low')


async def high_command(message: types.Message):
    logger.info(f"Получена команда /high с сообщением: {message.text}")
    await handle_price_command(message, 'high')


def register_handlers_low_high(dp: Dispatcher):
    # logger.info("Регистрация обработчиков для команд /low и /high")
    dp.message.register(low_command, Command("low"))
    dp.message.register(high_command, Command("high"))
    # logger.info("Обработчики команд /low и /high успешно зарегистрированы.")
