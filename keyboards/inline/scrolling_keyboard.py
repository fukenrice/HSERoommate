from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

scrolling_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="\N{THUMBS UP SIGN}", callback_data="yes"),
            InlineKeyboardButton(text="\N{THUMBS DOWN SIGN}", callback_data="no"),
            InlineKeyboardButton(text="\N{Octagonal Sign}", callback_data="stop"),
        ]
    ]
)
