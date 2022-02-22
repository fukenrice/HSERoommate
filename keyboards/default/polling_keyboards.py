from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

roommate_gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Муж"),
            KeyboardButton("Жен")
        ],
        [
            KeyboardButton("Неважно")
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

smoking_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Да"),
            KeyboardButton("Только электронные сигареты"),
            KeyboardButton("Нет")
        ]
    ], resize_keyboard=True
)

how_long_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Менее месяца"),
            KeyboardButton("От месяца до полугода"),
            KeyboardButton("Более полугода")
        ]
    ], resize_keyboard=True
)

location_global_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Внутри ЦАО"),
            KeyboardButton("В пределах ТТК"),
            KeyboardButton("В пределах МКАД"),
            KeyboardButton("За МКАД")
        ],
        [
            KeyboardButton("Неважно")
        ]
    ], resize_keyboard=True
)

location_local_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Запад"),
            KeyboardButton("Восток"),
            KeyboardButton("Север"),
            KeyboardButton("Юг")
        ],
        [
            KeyboardButton("Неважно")
        ]
    ], resize_keyboard=True
)

budget_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("10-15к"),
            KeyboardButton("15-25к"),
            KeyboardButton("25-35к"),
            KeyboardButton("35к+")
        ],
        [
            KeyboardButton("Неважно")
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
            KeyboardButton("Неважно")
        ]
    ], resize_keyboard=True
)
