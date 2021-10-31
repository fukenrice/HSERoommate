from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

scrolling_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("\N{THUMBS UP SIGN}"),
            KeyboardButton("\N{THUMBS DOWN SIGN}"),
            KeyboardButton("\N{Octagonal Sign}"),
        ]
    ], resize_keyboard=True
)
