from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp
from states.general_states import GeneralStates


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Привет, {message.from_user.full_name}!\nДля того, чтобы найти идеального соседа, воспользуйся этой небольшой инструкцией:\n\n1) создай и заполни анкету\n2) посмотри другие анкеты и лайкни понравившиеся\n3) жди сообщения от твоего нового соседа, либо напиши ему сам (в случае, если он лайкнул тебя)\n\nА в случае, если что-то непонятно, не стесняйся нажимать команду help - там ты найдёшь ответы на все вопросы.\n\nГотов начать? Нажимай команду new_form.", reply_markup=types.ReplyKeyboardRemove())
    await GeneralStates.main_menu.set()
