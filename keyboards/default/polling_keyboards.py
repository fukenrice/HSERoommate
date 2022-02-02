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

gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Муж"),
            KeyboardButton("Жен")
        ]
    ], resize_keyboard=True
)

binary_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Да"),
            KeyboardButton("Нет")
        ]
    ], resize_keyboard=True
)

room_num_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("1-2"),
            KeyboardButton("2-3"),
            KeyboardButton("3-4"),
        ],
        [
            KeyboardButton("Не важно")
        ]
    ]
)
