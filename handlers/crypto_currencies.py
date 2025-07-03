from aiogram import types, Dispatcher
from aiogram.filters import Command
from api.currency_api import get_popular_crypto_currencies


# Функция для разбиения текста на части
def split_text(text, max_length=4096):
    parts = []
    while len(text) > max_length:
        part = text[:max_length]
        last_newline = part.rfind('\n')
        if last_newline == -1:
            last_newline = max_length
        parts.append(part[:last_newline])
        text = text[last_newline:]
    parts.append(text)
    return parts

# Обработчик /crypto_currencies
async def crypto_currencies_command(message: types.Message):
    crypto_currencies = await get_popular_crypto_currencies()
    if crypto_currencies:
        crypto_list = "Популярные криптовалюты и их символы:\n"
        crypto_list += '\n'.join([f"{name} - {symbol}" for name, symbol in crypto_currencies.items()])

        # Разбиваем текст
        parts = split_text(crypto_list)
        for part in parts:
            await message.answer(part)
    else:
        await message.answer("Не удалось загрузить список криптовалют. Попробуйте позже.")



# Регистрация обработчиков
def register_handlers_crypto_currencies(dp: Dispatcher):
    dp.message.register(crypto_currencies_command, Command('crypto_currencies'))
