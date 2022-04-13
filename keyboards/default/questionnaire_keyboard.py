from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

my_questionnaire_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Редактировать анкету"),
            KeyboardButton(text="Удалить анкету"),
        ],
        [
            KeyboardButton(text="Назад")
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
            KeyboardButton(text="Местоположение"),
            KeyboardButton(text="Местоположение (уточн.)")
        ],
        [
            KeyboardButton(text="Бюджет"),
            KeyboardButton(text="Длительность проживания")
        ],
        [
            KeyboardButton(text="Квартира"),
            KeyboardButton(text="Животные"),
            KeyboardButton(text="Фото")
        ]
    ], resize_keyboard=True
)
