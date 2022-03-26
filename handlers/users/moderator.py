from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboards.default import moderator_keyboard
from loader import dp, bot, db
from models.questionnaire import Questionnaire
from states.modedator_states import ModeratorStates
from data.config import MODERATORS as moders


async def show_next(msg: types.Message, state: FSMContext):
    record = db.get_next_reported_que()
    if record is None:
        await msg.answer(text="Пока чисто, работы нет", reply_markup=types.ReplyKeyboardRemove())
    else:
        id = record[1]
        while not db.questionnaire_in_table(telegram_id=id):
            db.delete_from_reported(id)
        que = Questionnaire(db.get_questionnaire_by_urser_id(id))
        await msg.answer_photo(photo=que.photo, caption=str(que), reply_markup=moderator_keyboard)
        await ModeratorStates.moderating.set()
        async with state.proxy() as data:
            data["current_id"] = id


@dp.message_handler(lambda msg: msg.text.lower() == "reports" and str(msg.from_user.id) in moders, state="*")
async def start(msg: types.Message, state: FSMContext):
    await show_next(msg, state)


@dp.message_handler(lambda msg: msg.text in ["Оставить", "Удалить"] and str(msg.from_user.id) in moders, state=ModeratorStates.moderating)
async def moderating_result(msg: types.Message, state: FSMContext):
    if msg.text == "Удалить":
        async with state.proxy() as data:
            id = data["current_id"]
            if db.questionnaire_in_table(telegram_id=id):
                try:
                    db.delete_questionnaire(id)
                    await bot.send_message(chat_id=id, text="Ваша анкета была удалена модератором за нарушение правил сообщества")
                except Exception:
                    pass
    async with state.proxy() as data:
        id = data["current_id"]
        db.delete_from_reported(id)
    await show_next(msg, state)
