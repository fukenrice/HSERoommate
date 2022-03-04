from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


moderator_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Оставить"),
            KeyboardButton("Удалить"),
        ],
    ], resize_keyboard=True
)
