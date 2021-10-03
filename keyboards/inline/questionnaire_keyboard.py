from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

my_questionnaire_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Удалить анкету", callback_data="delete"),
            InlineKeyboardButton(text="Редактировать анкету", callback_data="edit")
        ]
    ]
)

edit_questionnaire_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Пол", callback_data="change_gender"),
            InlineKeyboardButton(text="Пол соседа", callback_data="change_roommate_gender"),
            InlineKeyboardButton(text="Имя", callback_data="change_name")
        ],
        [
            InlineKeyboardButton(text="Возраст", callback_data="change_age"),
            InlineKeyboardButton(text="Курение", callback_data="change_smoking"),
            InlineKeyboardButton(text="О себе", callback_data="change_about")
        ],
        [
            InlineKeyboardButton(text="Фото", callback_data="change_photo")
        ]
    ]
)




