from aiogram import types
from aiogram import Dispatcher
from aiogram.filters import Command
from api.currency_api import get_fiat_price, get_crypto_price
import logging

logger = logging.getLogger(__name__)

# Обработчик команды /convert
async def convert_command(message: types.Message):
    logger.info(f"Получена команда /convert с сообщением: {message.text}")
    args = message.text.strip().split()[1:]
    logger.info(f"Аргументы команды: {args}")

    if len(args) != 3:
        await message.answer("Используйте формат: /convert <сумма> <из валюты> <в валюту>. Например: /convert 100 USD RUB")
        return

    try:
        amount = float(args[0])
        if amount <= 0:
            await message.answer("Сумма должна быть положительным числом.")
            return
        from_currency = args[1].upper()
        to_currency = args[2].upper()
    except ValueError:
        await message.answer("Неверный формат суммы. Введите число.")
        return

    # Получаем курсы валют
    from_rate = await get_fiat_price(from_currency) or get_crypto_price(from_currency)
    to_rate = await get_fiat_price(to_currency) or get_crypto_price(to_currency)

    # Логируем курсы валют
    logger.info(f"Курс для {from_currency}: {from_rate}")
    logger.info(f"Курс для {to_currency}: {to_rate}")

    if from_rate is None:
        await message.answer(f"Валюта {from_currency} не найдена. Проверьте символ и попробуйте снова.")
        return
    if to_rate is None:
        await message.answer(f"Валюта {to_currency} не найдена. Проверьте символ и попробуйте снова.")
        return

    converted_amount = (amount / from_rate) * to_rate
    await message.answer(f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")

# Регистрация обработчика
def register_handlers_convert(dp: Dispatcher):
    dp.message.register(convert_command, Command('convert', ignore_case=True, prefix="/"))