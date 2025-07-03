from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура с основными командами
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/start")],
            [KeyboardButton(text="/help")],
            [KeyboardButton(text="/price")],
            [KeyboardButton(text="/low")],
            [KeyboardButton(text="/high")],
            [KeyboardButton(text="/convert")],
            [KeyboardButton(text="/currencies")],
            [KeyboardButton(text="/crypto_currencies")],
            [KeyboardButton(text="/history")],
        ],
        resize_keyboard=True # Автоматически изменяет размер клавиатуры
    )
    return keyboard
