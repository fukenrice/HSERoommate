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
            InlineKeyboardButton(text="Неважно", callback_data="Неважно")
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

room_num_keyboard = InlineKeyboardMarkup (
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1-2", callback_data="1-2"),
            InlineKeyboardButton(text="2-3", callback_data="2-3"),
            InlineKeyboardButton(text="3-4", callback_data="3-4")
        ],
        [
            InlineKeyboardButton(text="Не важно", callback_data="Не важно")
        ]
    ]
)


