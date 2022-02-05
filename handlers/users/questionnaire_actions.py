from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
import keyboards.inline as ik
from loader import dp, bot, db
from models import Questionnaire
from states.general_states import GeneralStates


@dp.message_handler(Command("my_questionnaire"), state="*")
async def show_questionnaire(msg: types.Message):
    if db.questionnaire_in_table(telegram_id=msg.from_user.id):
        questionnaire = Questionnaire(db.get_questionnaire_by_urser_id(msg.from_user.id))
        await msg.answer_photo(photo=questionnaire.photo, caption=f"Вот твоя анкета:\n"
                                                                  f"Пол: {questionnaire.gender}\n"
                                                                  f"Пол соседа: {questionnaire.roommate_gender}\n"
                                                                  f"{questionnaire}\n",
                               reply_markup=ik.my_questionnaire_keyboard)
        await GeneralStates.questionnaire_edit.set()

    else:
        await msg.answer(
            text="Хм, не могу найти твою анкету в базе, ты можешь создать ее с помощью команды /new_questionnaire",
            reply_markup=types.ReplyKeyboardRemove())


@dp.callback_query_handler(text="delete", state=GeneralStates.questionnaire_edit)
async def delete_questionnaire(callback: types.CallbackQuery, state: FSMContext):
    db.delete_questionnaire(callback.from_user.id)
    await callback.answer(text="Акета удалена")
    await bot.send_message(text="Ваша акета успешно удалена, ее больше никто не увидит."
                                " В любой момент вы можете создать новую при помощи команды /new_questionnaire",
                           chat_id=callback.from_user.id)
    await state.finish()


@dp.callback_query_handler(text="edit", state=GeneralStates.questionnaire_edit)
async def show_edit_menu(callback: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_reply_markup(chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=ik.edit_questionnaire_keyboard)
    await GeneralStates.questionnaire_editing_field.set()


@dp.callback_query_handler(text="change_gender", state=GeneralStates.questionnaire_editing_field)
async def change_gender(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=callback.from_user.id, text="Ваш пол?", reply_markup=ik.gender_keyboard)
    await GeneralStates.edited_gender.set()


@dp.callback_query_handler(state=GeneralStates.edited_gender)
async def apply_gender(callback: types.CallbackQuery, state: FSMContext):
    db.change_field('gender', f"'{callback.data}'", telegram_id=callback.from_user.id)
    await bot.send_message(chat_id=callback.from_user.id, text="Ваш пол успешно изменен")
    await state.finish()


@dp.callback_query_handler(text="change_roommate_gender", state=GeneralStates.questionnaire_editing_field)
async def change_roommate_gender(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.from_user.id, text="Жлеаемый пол соседа?", reply_markup=ik.roommate_gender_keyboard)
    await GeneralStates.edited_roommate_gender.set()


@dp.callback_query_handler(state=GeneralStates.edited_roommate_gender)
async def apply_roommate_gender(callback: types.CallbackQuery, state: FSMContext):
    db.change_field('roommate_gender', f"'{callback.data}'", telegram_id=callback.from_user.id)
    await bot.send_message(chat_id=callback.from_user.id, text="Пол соседа успешно изменен")
    await state.finish()


@dp.callback_query_handler(text="change_name", state=GeneralStates.questionnaire_editing_field)
async def change_name(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.from_user.id, text="Введите имя")
    await GeneralStates.edited_name.set()


@dp.message_handler(state=GeneralStates.edited_name)
async def apply_name(msg: types.Message, state: FSMContext):
    db.change_field('name', f"'{msg.text[:40]}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Имя успешно изменено")
    await state.finish()


@dp.callback_query_handler(text="change_age", state=GeneralStates.questionnaire_editing_field)
async def change_age(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.from_user.id, text="Введите возраст")
    await GeneralStates.edited_age.set()


@dp.message_handler(state=GeneralStates.edited_age)
async def apply_age(msg: types.Message, state: FSMContext):
    if msg.text.isdigit() and 17 <= int(msg.text) <= 100:
        db.change_field('age', f'{msg.text}', telegram_id=msg.from_user.id)
        await msg.answer(text="Возраст успешно изменен")
        await state.finish()
    else:
        await msg.answer(text="Введен некорректный возраст, попробуйте снова(от 17 лет)")


@dp.callback_query_handler(text="change_smoking", state=GeneralStates.questionnaire_editing_field)
async def change_smoking(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.from_user.id, text="Курите?", reply_markup=ik.binary_keyboard)
    await GeneralStates.edited_smoking.set()


@dp.callback_query_handler(state=GeneralStates.edited_smoking)
async def apply_smoking(callback: types.CallbackQuery, state: FSMContext):
    db.change_field('smoking', f'{callback.data}', telegram_id=callback.from_user.id)
    await bot.send_message(chat_id=callback.from_user.id, text="Курение успешно изменено!")
    await state.finish()


@dp.callback_query_handler(text="change_about", state=GeneralStates.questionnaire_editing_field)
async def change_about(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.from_user.id, text="Расскажите о себе")
    await GeneralStates.edited_about.set()


@dp.message_handler(state=GeneralStates.edited_about)
async def apply_about(msg: types.Message, state: FSMContext):
    db.change_field('about', f"'{msg.text[:869]}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Описание успешно изменено!")
    await state.finish()


@dp.callback_query_handler(text="change_photo", state=GeneralStates.questionnaire_editing_field)
async def changing_photo(callback: types.CallbackQuery):
    await bot.send_message(chat_id=callback.from_user.id, text="Отправьте мне новую фотографию")
    await GeneralStates.edited_photo.set()


@dp.message_handler(content_types=["photo"], state=GeneralStates.edited_photo)
async def apply_photo(msg: types.Message, state: FSMContext):
    db.change_field('photo_id', f"'{msg.photo[-1].file_id}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Фото успешно изменено!")
    await state.finish()
