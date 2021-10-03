from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

gender_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Муж", callback_data="Мужской"),
            InlineKeyboardButton(text="Жен", callback_data="Женский"),
        ]
    ]
)

roommate_gender_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Муж", callback_data="Мужской"),
            InlineKeyboardButton(text="Жен", callback_data="Женский"),
        ],
        [
            InlineKeyboardButton(text="Не важно", callback_data="Не важно")
        ]
    ]
)

binary_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="1"),
            InlineKeyboardButton(text="Нет", callback_data="0")
        ]
    ]
)



