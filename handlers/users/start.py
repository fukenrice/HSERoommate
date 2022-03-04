from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.default import main_keyboard
from loader import dp
from states.general_states import GeneralStates


@dp.message_handler(lambda msg: msg.text in ["/start", "Главное меню"], state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Привет, {message.from_user.full_name}!\nДля того, чтобы найти идеального соседа, воспользуйся этой небольшой инструкцией:\n"
                         f"\n1) создай и заполни анкету\n"
                         f"2) посмотри другие анкеты и лайкни понравившиеся\n"
                         f"3) жди сообщения от твоего нового соседа, либо напиши ему сам (в случае, если он лайкнул тебя)\n"
                         f"\nА в случае, если что-то непонятно, не стесняйся нажимать команду help - там ты найдёшь ответы на все вопросы.\n"
                         f"\nГотов начать? Нажимай команду /new_form.", reply_markup=main_keyboard)
    await GeneralStates.main_menu.set()
