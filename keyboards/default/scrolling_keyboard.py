from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

scrolling_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("\N{THUMBS UP SIGN}"),
            KeyboardButton("\N{THUMBS DOWN SIGN}"),
            KeyboardButton("\N{Squared Sos} Пожаловаться"),
        ],
        [
            KeyboardButton("\N{Octagonal Sign} Остановить поиск"),
        ]
    ], resize_keyboard=True
)
