from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Главное меню"),
            KeyboardButton("Заполнить новую анкету"),
        ],
        [
            KeyboardButton("Редактировать свою анкету"),
            KeyboardButton("Посмотреть анкеты")
        ],
        [
            KeyboardButton("Помощь")
        ]
    ], resize_keyboard=True
)
