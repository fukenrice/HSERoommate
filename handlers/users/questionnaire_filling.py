from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types.message import ContentType

from keyboards.default import gender_keyboard, roommate_gender_keyboard, binary_keyboard, room_num_keyboard,\
    how_long_keyboard, smoking_keyboard, budget_keyboard, location_local_keyboard, location_global_keyboard, main_keyboard
from loader import dp, bot, db
from states.questionnaire_states import QuestionnaireStates
from states.general_states import GeneralStates


@dp.message_handler(lambda msg: msg.text in ["/new_form", "Заполнить новую анкету"], state="*")
async def start_polling(msg: types.Message, state: FSMContext):
    await GeneralStates.main_menu.set()
    if db.questionnaire_in_table(telegram_id=msg.from_user.id):
        await msg.answer(text="Твоя анкета уже находится в базе, ты можешь ее удалить, а потом создать новую.", reply_markup=main_keyboard)
        await state.finish()
    else:
        await msg.answer(text="Как тебя зовут?", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        await QuestionnaireStates.name_question.set()


@dp.message_handler(state=QuestionnaireStates.name_question)
async def age_question(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text[:20])
    await msg.answer(text="Твой возраст?")
    await QuestionnaireStates.age_question.set()


@dp.message_handler(state=QuestionnaireStates.age_question)
async def gender_question(msg: types.Message, state: FSMContext):
    if msg.text.isdigit() and 17 <= int(msg.text) <= 100:
        await state.update_data(age=msg.text)
        await msg.answer(text="Твой пол?", reply_markup=gender_keyboard)
        await QuestionnaireStates.gender_question.set()
    else:
        await msg.answer("Введен некорректный возраст, попробуй снова(от 17 лет)")


@dp.message_handler(lambda msg: msg.text in ["Муж", "Жен"], state=QuestionnaireStates.gender_question)
async def roommate_gender_question(msg: types.Message, state: FSMContext):
    await state.update_data(gender=msg.text)
    await msg.answer(text="Желаемый пол соседа?", reply_markup=roommate_gender_keyboard)
    await QuestionnaireStates.roommate_gender_question.set()


@dp.message_handler(lambda msg: msg.text in ["Муж", "Жен", "Неважно"], state=QuestionnaireStates.roommate_gender_question)
async def how_long_question(msg: types.Message, state: FSMContext):
    await state.update_data(roommate_gender=msg.text)
    await msg.answer(text="В течение какого времени ты хочешь снимать квартиру?", reply_markup=how_long_keyboard)
    await QuestionnaireStates.how_long_question.set()


@dp.message_handler(lambda msg: msg.text in ["Менее месяца", "От месяца до полугода", "Более полугода"], state=QuestionnaireStates.how_long_question)
async def location_global_question(msg: types.Message, state: FSMContext):
    await state.update_data(how_long=msg.text)
    await msg.answer(text="Где бы ты хотел жить?", reply_markup=location_global_keyboard)
    await QuestionnaireStates.location_global_question.set()


@dp.message_handler(lambda msg: msg.text in ["Внутри ЦАО", "В пределах ТТК", "В пределах МКАД", "За МКАД", "Неважно"], state=QuestionnaireStates.location_global_question)
async def location_local_question(msg: types.Message, state: FSMContext):
    await state.update_data(location_global=msg.text)
    await msg.answer(text="А точнее?", reply_markup=location_local_keyboard)
    await QuestionnaireStates.location_local_question.set()


@dp.message_handler(lambda msg: msg.text in ["Запад", "Восток", "Север", "Юг", "Неважно"], state=QuestionnaireStates.location_local_question)
async def pet_question(msg: types.Message, state: FSMContext):
    await state.update_data(location_local=msg.text)
    await msg.answer(text="Готов ли ты жить с соседом, у которого будет домашнее животное?", reply_markup=binary_keyboard)
    await QuestionnaireStates.pet_question.set()


@dp.message_handler(lambda msg: msg.text in ["Да", "Нет"], state=QuestionnaireStates.pet_question)
async def budget_question(msg: types.Message, state: FSMContext):
    await state.update_data(pet=msg.text)
    await msg.answer(text="Каков твой бюджет для аренды квартиры? (с человека)", reply_markup=budget_keyboard)
    await QuestionnaireStates.budget_question.set()


@dp.message_handler(lambda msg: msg.text in ["10-15к", "15-25к", "25-35к", "35к+"], state=QuestionnaireStates.budget_question)
async def apartment_question(msg: types.Message, state: FSMContext):
    await state.update_data(budget=msg.text)
    await msg.answer(text="Нашел ли ты уже квартиру?", reply_markup=binary_keyboard)
    await QuestionnaireStates.apartment_question.set()

@dp.message_handler(lambda msg: msg.text in ["Да", "Нет"], state=QuestionnaireStates.apartment_question)
async def smoking_question(msg: types.Message, state: FSMContext):
    await state.update_data(apartment=msg.text)
    await msg.answer(text="Ты куришь?", reply_markup=smoking_keyboard)
    await QuestionnaireStates.smoking_question.set()


@dp.message_handler(lambda msg: msg.text in ["Да", "Только электронные сигареты", "Нет"], state=QuestionnaireStates.smoking_question)
async def rooms_number_question(msg: types.Message, state: FSMContext):
    await state.update_data(smoking=msg.text)
    await msg.answer(text="Желаемое количество комнат?", reply_markup=room_num_keyboard)
    await QuestionnaireStates.rooms_number_question.set()


@dp.message_handler(lambda msg: msg.text in ["1-2", "2-3", "3-4", "Неважно"], state=QuestionnaireStates.rooms_number_question)
async def about_question(msg: types.Message, state: FSMContext):
    await state.update_data(rooms_number=str(msg.text))
    await msg.answer(text="Расскажи немного о себе, чтобы дать потенциальному соседу больше информации", reply_markup=types.ReplyKeyboardRemove())
    await QuestionnaireStates.about_question.set()


@dp.message_handler(state=QuestionnaireStates.about_question)
async def photo_question(msg: types.Message, state: FSMContext):
    await state.update_data(about=msg.text[:799])
    await msg.answer(text="Отлично, для завершения заполнения анкеты отправь мне свою фотографию", reply_markup=types.ReplyKeyboardRemove())
    await QuestionnaireStates.end_of_questionnaire.set()


@dp.message_handler(lambda msg: msg.content_type != ContentType.PHOTO, state=QuestionnaireStates.end_of_questionnaire)
async def photo_reminder(msg: types.message):
    await msg.answer(text="Пожалуйста отправь мне фотографию(не как файл)")


@dp.message_handler(content_types=["photo"], state=QuestionnaireStates.end_of_questionnaire)
async def end_of_questionnaire(msg: types.Message, state: FSMContext):
    await state.update_data(photo=msg.photo[-1].file_id)
    msg.content_type
    data = await state.get_data()
    db.add_user(msg.from_user.id, data.get("name"), int(data.get("age")), data.get("gender"),
                data.get("roommate_gender"), (lambda: 1 if data.get("smoking") == "Да" else 0)(),
                data.get("rooms_number"), data.get("about"),
                data.get("photo"), data.get("how_long"), data.get("location_global"), data.get("location_local"),
                data.get("pet"), data.get("budget"), data.get("apartment"))
    await msg.answer(text="Твоя анкета успешно добавлена в базу! Теперь ты можешь искать соседа, удачи в поисках!\nДля этого нажми /show",
                     reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
