from aiogram import types
from aiogram import Dispatcher
from aiogram.filters import Command


# Обработчик команды /help
async def help_command(message: types.Message):
    help_text = (
        "*Доступные команды:*\n"
        "• `/start` — Запуск бота\n"
        "• `/help` — Помощь\n"
        "• `/price <символ валюты>` — Получить текущий курс валюты\n"
        "• `/low <символ валюты>` — Минимальный курс за неделю\n"
        "• `/high <символ валюты>` — Максимальный курс за неделю\n"
        "• `/convert <сумма> <из валюты> <в валюту>` — Конвертировать сумму\n"
        "• `/currencies` — Список доступных фиатных валют\n"
        "• `/crypto_currencies` — Список доступных криптовалют\n"
        "• `/history` — История ваших запросов\n"
    )
    await message.answer(help_text, parse_mode="Markdown")

# Регистрация обработчика
def register_handlers_help(dp: Dispatcher):
    dp.message.register(help_command, Command('help'))




