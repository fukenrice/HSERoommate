from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher import FSMContext
from loader import dp


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message, state: FSMContext):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")
    
    await message.answer("\n".join(text))
    await state.finish()
