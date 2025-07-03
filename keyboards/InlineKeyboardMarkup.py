from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Inline-клавиатура для выбора валюты
def get_currency_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="USD", callback_data="currency_USD"),
                InlineKeyboardButton(text="EUR", callback_data="currency_EUR"),
                InlineKeyboardButton(text="RUB", callback_data="currency_RUB"),
            ],
            [
                InlineKeyboardButton(text="BTC", callback_data="currency_BTC"),
                InlineKeyboardButton(text="ETH", callback_data="currency_ETH"),
                InlineKeyboardButton(text="DOGE", callback_data="currency_DOGE"),
            ],
        ],
        row_width=3  # количество кнопок в строке
    )
    return keyboard



