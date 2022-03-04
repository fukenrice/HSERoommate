from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

import keyboards.default as keyboard
from keyboards.default import main_keyboard
from loader import dp, bot, db
from models import Questionnaire
from states.general_states import GeneralStates


@dp.message_handler(lambda msg: msg.text in ["/my_form", "Редактировать свою анкету"], state="*")
async def show_questionnaire(msg: types.Message):
    if db.questionnaire_in_table(telegram_id=msg.from_user.id):
        questionnaire = Questionnaire(db.get_questionnaire_by_urser_id(msg.from_user.id))
        await msg.answer_photo(photo=questionnaire.photo, caption=f"Вот твоя анкета:\n"
                                                                  f"{questionnaire}\n"
                                                                  f"Пол: {questionnaire.gender}\n"
                                                                  f"Пол соседа: {questionnaire.roommate_gender}",
                               reply_markup=keyboard.my_questionnaire_keyboard)
        await GeneralStates.questionnaire_edit.set()

    else:
        await msg.answer(
            text="Хм, не могу найти твою анкету в базе, ты можешь создать ее с помощью команды /new_form",
            reply_markup=main_keyboard)


@dp.message_handler(lambda msg: msg.text == "Удалить анкету", state=GeneralStates.questionnaire_edit)
async def delete_questionnaire(msg: types.Message, state: FSMContext):
    db.delete_questionnaire(msg.from_user.id)
    await msg.answer(text="Твоя акета успешно удалена, ее больше никто не увидит."
                          " В любой момент ты можешь создать новую при помощи команды /new_form",
                     reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Редактировать анкету", state=GeneralStates.questionnaire_edit)
async def show_edit_menu(msg: types.Message, state: FSMContext):
    await msg.answer(text="Что ты хочешь изменить?", reply_markup=keyboard.edit_questionnaire_keyboard)
    await GeneralStates.questionnaire_editing_field.set()


@dp.message_handler(lambda msg: msg.text == "Пол", state=GeneralStates.questionnaire_editing_field)
async def change_gender(msg: types.Message, state: FSMContext):
    await msg.answer(text="Твой пол?", reply_markup=keyboard.gender_keyboard)
    await GeneralStates.edited_gender.set()


@dp.message_handler(lambda msg: msg.text in ["Муж", "Жен"], state=GeneralStates.edited_gender)
async def apply_gender(msg: types.Message, state: FSMContext):
    db.change_field('gender', f"'{msg.text}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Твой пол успешно изменен", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Длительность проживания", state=GeneralStates.questionnaire_editing_field)
async def change_how_long(msg: types.Message, state: FSMContext):
    await msg.answer(text="В течение какого времени ты хочешь снимать квартиру?", reply_markup=keyboard.how_long_keyboard)
    await GeneralStates.edited_how_long.set()


@dp.message_handler(lambda msg: msg.text in ["Менее месяца", "От месяца до полугода", "Более полугода"], state=GeneralStates.edited_how_long)
async def apply_how_long(msg: types.Message, state: FSMContext):
    db.change_field('how_long', f"'{msg.text}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Длительность проживания успешно изменена", reply_markup=main_keyboard)
    await state.finish()

@dp.message_handler(lambda msg: msg.text == "Бюджет", state=GeneralStates.questionnaire_editing_field)
async def change_budget(msg: types.Message, state: FSMContext):
    await msg.answer(text="Каков твой бюджет для аренды квартиры?", reply_markup=keyboard.budget_keyboard)
    await GeneralStates.edited_budget.set()


@dp.message_handler(lambda msg: msg.text in ["10-15к", "15-25к", "25-35к", "35к+", "Неважно"], state=GeneralStates.edited_budget)
async def apply_budget(msg: types.Message, state: FSMContext):
    db.change_field('budget', f"'{msg.text}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Бюджет успешно изменен", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Местоположение", state=GeneralStates.questionnaire_editing_field)
async def change_location_global(msg: types.Message, state: FSMContext):
    await msg.answer(text="Где бы ты хотел жить?", reply_markup=keyboard.location_global_keyboard)
    await GeneralStates.edited_location_global.set()


@dp.message_handler(lambda msg: msg.text in ["Внутри ЦАО", "В пределах ТТК", "В пределах МКАД", "За МКАД", "Неважно"], state=GeneralStates.edited_location_global)
async def apply_location_global(msg: types.Message, state: FSMContext):
    db.change_field('location', f"'{msg.text}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Местоположение успешно изменено", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Местоположение (уточн.)", state=GeneralStates.questionnaire_editing_field)
async def change_location_local(msg: types.Message, state: FSMContext):
    await msg.answer(text="Где бы ты хотел жить (уточн.)?", reply_markup=keyboard.location_local_keyboard)
    await GeneralStates.edited_location_local.set()


@dp.message_handler(lambda msg: msg.text in ["Запад", "Восток", "Север", "Юг", "Неважно"], state=GeneralStates.edited_location_local)
async def apply_location_local(msg: types.Message, state: FSMContext):
    db.change_field('local_location', f"'{msg.text}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Местоположение успешно изменено", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Квартира", state=GeneralStates.questionnaire_editing_field)
async def change_apartment(msg: types.Message, state: FSMContext):
    await msg.answer(text="Нашел ли ты уже квартиру?", reply_markup=keyboard.binary_keyboard)
    await GeneralStates.edited_apartment.set()


@dp.message_handler(lambda msg: msg.text in ["Да", "Нет"], state=GeneralStates.edited_apartment)
async def apply_apartment(msg: types.Message, state: FSMContext):
    db.change_field('found', f"'{msg.text}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Данные о квартире успешно изменены", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Животные", state=GeneralStates.questionnaire_editing_field)
async def change_pet(msg: types.Message, state: FSMContext):
    await msg.answer(text="Готов ли ты жить с соседом, у которого будет домашнее животное?", reply_markup=keyboard.binary_keyboard)
    await GeneralStates.edited_pet.set()


@dp.message_handler(lambda msg: msg.text in ["Да", "Нет"], state=GeneralStates.edited_pet)
async def apply_pet(msg: types.Message, state: FSMContext):
    db.change_field('pet', f"'{msg.text}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Данные о животных успешно изменены", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Пол соседа", state=GeneralStates.questionnaire_editing_field)
async def change_roommate_gender(msg: types.Message):
    await msg.answer(text="Жлеаемый пол соседа?", reply_markup=keyboard.roommate_gender_keyboard)
    await GeneralStates.edited_roommate_gender.set()


@dp.message_handler(lambda msg: msg.text in ["Муж", "Жен", "Не важно"], state=GeneralStates.edited_roommate_gender)
async def apply_roommate_gender(msg: types.Message, state: FSMContext):
    db.change_field('roommate_gender', f"'{msg.text}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Пол соседа успешно изменен", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Имя", state=GeneralStates.questionnaire_editing_field)
async def change_name(msg: types.Message):
    await msg.answer(text="Введи имя", reply_markup=types.ReplyKeyboardRemove())
    await GeneralStates.edited_name.set()


@dp.message_handler(state=GeneralStates.edited_name)
async def apply_name(msg: types.Message, state: FSMContext):
    db.change_field('name', f"'{msg.text[:40]}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Имя успешно изменено", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Возраст", state=GeneralStates.questionnaire_editing_field)
async def change_age(msg: types.Message):
    await msg.answer(text="Введи возраст", reply_markup=types.ReplyKeyboardRemove())
    await GeneralStates.edited_age.set()


@dp.message_handler(state=GeneralStates.edited_age)
async def apply_age(msg: types.Message, state: FSMContext):
    if msg.text.isdigit() and 17 <= int(msg.text) <= 100:
        db.change_field('age', f'{msg.text}', telegram_id=msg.from_user.id)
        await msg.answer(text="Возраст успешно изменен", reply_markup=main_keyboard)
        await state.finish()
    else:
        await msg.answer(text="Введен некорректный возраст, попробуй снова(от 17 лет)",
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda msg: msg.text == "Курение", state=GeneralStates.questionnaire_editing_field)
async def change_smoking(msg: types.Message):
    await msg.answer(text="Ты куришь?", reply_markup=keyboard.smoking_keyboard)
    await GeneralStates.edited_smoking.set()


@dp.message_handler(lambda msg: msg.text in ["Да", "Только электронные сигареты", "Нет"], state=GeneralStates.edited_smoking)
async def apply_smoking(msg: types.Message, state: FSMContext):
    db.change_field('smoking', f"{(lambda: 1 if msg.text == 'Да' else 0)()}", telegram_id=msg.from_user.id)
    await msg.answer(text="Курение успешно изменено!", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "О себе", state=GeneralStates.questionnaire_editing_field)
async def change_about(msg: types.Message):
    await msg.answer(text="Расскажи о себе", reply_markup=types.ReplyKeyboardRemove())
    await GeneralStates.edited_about.set()


@dp.message_handler(state=GeneralStates.edited_about)
async def apply_about(msg: types.Message, state: FSMContext):
    db.change_field('about', f"'{msg.text[:869]}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Описание успешно изменено!", reply_markup=main_keyboard)
    await state.finish()


@dp.message_handler(lambda msg: msg.text == "Фото", state=GeneralStates.questionnaire_editing_field)
async def changing_photo(msg: types.Message):
    await msg.answer(text="Отправь мне новую фотографию", reply_markup=types.ReplyKeyboardRemove())
    await GeneralStates.edited_photo.set()


@dp.message_handler(content_types=["photo"], state=GeneralStates.edited_photo)
async def apply_photo(msg: types.Message, state: FSMContext):
    db.change_field('photo_id', f"'{msg.photo[-1].file_id}'", telegram_id=msg.from_user.id)
    await msg.answer(text="Фото успешно изменено!", reply_markup=main_keyboard)
    await state.finish()
