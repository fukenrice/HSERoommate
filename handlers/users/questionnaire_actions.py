from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

import keyboards.default as keyboard
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
                               reply_markup=keyboard.my_questionnaire_keyboard)
        await GeneralStates.questionnaire_edit.set()

    else:
        await msg.answer(
            text="Хм, не могу найти твою анкету в базе, ты можешь создать ее с помощью команды /new_questionnaire",
            reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda msg: msg.text == "Удалить анкету", state=GeneralStates.questionnaire_edit)
async def delete_questionnaire(msg: types.Message, state: FSMContext):
    db.delete_questionnaire(msg.from_user.id)
    await msg.answer(text="Ваша акета успешно удалена, ее больше никто не увидит."
                          " В любой момент вы можете создать новую при помощи команды /new_questionnaire",
                     reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Редактировать анкету", state=GeneralStates.questionnaire_edit)
async def show_edit_menu(msg: types.Message, state: FSMContext):
    await msg.answer(text="Что вы хотите изменить?", reply_markup=keyboard.edit_questionnaire_keyboard)
    await GeneralStates.questionnaire_editing_field.set()


@dp.message_handler(lambda msg: msg.text == "Пол", state=GeneralStates.questionnaire_editing_field)
async def change_gender(msg: types.Message, state: FSMContext):
    await msg.answer(text="Ваш пол?", reply_markup=keyboard.gender_keyboard)
    await GeneralStates.edited_gender.set()


@dp.message_handler(lambda msg: msg.text in ["Муж", "Жен"], state=GeneralStates.edited_gender)
async def apply_gender(msg: types.Message, state: FSMContext):
    db.change_field('gender', f"'{msg.text}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Ваш пол успешно изменен", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Пол соседа", state=GeneralStates.questionnaire_editing_field)
async def change_roommate_gender(msg: types.Message):
    await msg.answer(text="Жлеаемый пол соседа?", reply_markup=keyboard.roommate_gender_keyboard)
    await GeneralStates.edited_roommate_gender.set()


@dp.message_handler(lambda msg: msg.text in ["Муж", "Жен", "Не важно"], state=GeneralStates.edited_roommate_gender)
async def apply_roommate_gender(msg: types.Message, state: FSMContext):
    db.change_field('roommate_gender', f"'{msg.text}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Пол соседа успешно изменен", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Имя", state=GeneralStates.questionnaire_editing_field)
async def change_name(msg: types.Message):
    await msg.answer(text="Введите имя", reply_markup=types.ReplyKeyboardRemove())
    await GeneralStates.edited_name.set()


@dp.message_handler(state=GeneralStates.edited_name)
async def apply_name(msg: types.Message, state: FSMContext):
    db.change_field('name', f"'{msg.text[:40]}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Имя успешно изменено", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Возраст", state=GeneralStates.questionnaire_editing_field)
async def change_age(msg: types.Message):
    await msg.answer(text="Введите возраст", reply_markup=types.ReplyKeyboardRemove())
    await GeneralStates.edited_age.set()


@dp.message_handler(state=GeneralStates.edited_age)
async def apply_age(msg: types.Message, state: FSMContext):
    if msg.text.isdigit() and 17 <= int(msg.text) <= 100:
        db.change_field('age', f'{msg.text}', telegram_id=msg.from_user.id)
        await msg.answer(text="Возраст успешно изменен", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    else:
        await msg.answer(text="Введен некорректный возраст, попробуйте снова(от 17 лет)",
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda msg: msg.text == "Курение", state=GeneralStates.questionnaire_editing_field)
async def change_smoking(msg: types.Message):
    await msg.answer(text="Курите?", reply_markup=keyboard.binary_keyboard)
    await GeneralStates.edited_smoking.set()


@dp.message_handler(lambda msg: msg.text in ["Да", "Нет"], state=GeneralStates.edited_smoking)
async def apply_smoking(msg: types.Message, state: FSMContext):
    db.change_field('smoking', f"{(lambda: 1 if msg.text == 'Да' else 0)()}", telegram_id=msg.from_user.id)
    await msg.answer(text="Курение успешно изменено!", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "О себе", state=GeneralStates.questionnaire_editing_field)
async def change_about(msg: types.Message):
    await msg.answer(text="Расскажите о себе", reply_markup=types.ReplyKeyboardRemove())
    await GeneralStates.edited_about.set()


@dp.message_handler(state=GeneralStates.edited_about)
async def apply_about(msg: types.Message, state: FSMContext):
    db.change_field('about', f"'{msg.text[:869]}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Описание успешно изменено!", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Фото", state=GeneralStates.questionnaire_editing_field)
async def changing_photo(msg: types.Message):
    await msg.answer(text="Отправьте мне новую фотографию", reply_markup=types.ReplyKeyboardRemove())
    await GeneralStates.edited_photo.set()


@dp.message_handler(content_types=["photo"], state=GeneralStates.edited_photo)
async def apply_photo(msg: types.Message, state: FSMContext):
    db.change_field('photo_id', f"'{msg.photo[-1].file_id}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Фото успешно изменено!", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
