from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

my_questionnaire_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Удалить анктеу"),
            KeyboardButton(text="Редактировать анкету")
        ]
    ], resize_keyboard=True
)

edit_questionnaire_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Пол"),
            KeyboardButton(text="Пол соседа"),
            KeyboardButton(text="Имя")
        ],
        [
            KeyboardButton(text="Возраст"),
            KeyboardButton(text="Курение"),
            KeyboardButton(text="О себе")
        ],
        [
            KeyboardButton(text="Фото")
        ]
    ], resize_keyboard=True
)