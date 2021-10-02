from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

gender_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Муж", callback_data="male"),
            InlineKeyboardButton(text="Жен", callback_data="female"),
        ]
    ]
)

roommate_gender_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Муж", callback_data="male"),
            InlineKeyboardButton(text="Жен", callback_data="female"),
        ],
        [
            InlineKeyboardButton(text="Не важно", callback_data="no")
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



