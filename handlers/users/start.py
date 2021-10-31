from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp
from states.general_states import GeneralStates


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=types.ReplyKeyboardRemove())
    await GeneralStates.main_menu.set()
