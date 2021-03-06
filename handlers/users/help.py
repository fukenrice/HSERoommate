from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher import FSMContext
from keyboards.default import menu_keyboard
from loader import dp
from states.general_states import GeneralStates


@dp.message_handler(lambda msg: msg.text in ["/help", "Помощь"], state="*")
async def bot_help(message: types.Message, state: FSMContext):
    await GeneralStates.main_menu.set()
    text = ("Как отредактировать анкету?",
            "Выбери команду /my_form и нажми на соответствующую кнопку.\n",
            "Что делать, если бот лагает?",
            "Это связано с временной перегруженностью серверов - такое бывает крайне редко. Не волнуйся, в ближайшее время всё придёт в норму.\n",
            "Как удалить анкету?",
            "Нажми на /my_form и на кнопку удалить анкету.\n",
            "Что делать, если я не нашёл ответ на свой вопрос?",
            "Писать в лс @mayflowerq")

    await message.answer("\n".join(text), reply_markup=menu_keyboard.main_keyboard)
