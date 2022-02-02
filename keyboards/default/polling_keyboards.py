from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

roommate_gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Муж"),
            KeyboardButton("Жен")
        ],
        [
            KeyboardButton("Не важно")
        ]
    ], resize_keyboard=True
)

binary_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Муж"),
            KeyboardButton("Жен")
        ]
    ], resize_keyboard=True
)
