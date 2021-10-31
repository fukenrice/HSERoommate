from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher import FSMContext
from loader import dp
from states.general_states import GeneralStates

@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message, state: FSMContext):
    await GeneralStates.main_menu.set()
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")
    
    await message.answer("\n".join(text), reply_markup=types.ReplyKeyboardRemove())
