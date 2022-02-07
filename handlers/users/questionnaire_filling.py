from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from keyboards.default import gender_keyboard, roommate_gender_keyboard, binary_keyboard, room_num_keyboard
from loader import dp, bot, db
from states.questionnaire_states import QuestionnaireStates
from states.general_states import GeneralStates


@dp.message_handler(Command("new_form"), state="*")
async def start_polling(msg: types.Message, state: FSMContext):
    await GeneralStates.main_menu.set()
    if db.questionnaire_in_table(telegram_id=msg.from_user.id):
        await msg.answer(text="Ваша анкета уже находится в базе, вы можете ее удалить, а потом создать новую.")
        await state.finish()
    else:
        await msg.answer(text="Как вас зовут?")
        await state.finish()
        await QuestionnaireStates.name_question.set()


@dp.message_handler(state=QuestionnaireStates.name_question)
async def age_question(msg: types.Message, state: FSMContext):
    await state.update_data(name=msg.text[:20])
    await msg.answer(text="Ваш возраст?")
    await QuestionnaireStates.age_question.set()


@dp.message_handler(state=QuestionnaireStates.age_question)
async def gender_question(msg: types.Message, state: FSMContext):
    if msg.text.isdigit() and 17 <= int(msg.text) <= 100:
        await state.update_data(age=msg.text)
        await msg.answer(text="Ваш пол?", reply_markup=gender_keyboard)
        await QuestionnaireStates.gender_question.set()
    else:
        await msg.answer("Введен некорректный возраст, попробуйте снова(от 17 лет)")


@dp.message_handler(lambda msg: msg.text in ["Муж", "Жен"], state=QuestionnaireStates.gender_question)
async def roommate_gender_question(msg: types.Message, state: FSMContext):
    await state.update_data(gender=msg.text)
    await msg.answer(text="Желаемый пол соседа?", reply_markup=roommate_gender_keyboard)
    await QuestionnaireStates.roommate_gender_question.set()


@dp.message_handler(lambda msg: msg.text in ["Муж", "Жен", "Не важно"], state=QuestionnaireStates.roommate_gender_question)
async def smoking_question(msg: types.Message, state: FSMContext):
    await state.update_data(roommate_gender=msg.text)
    await msg.answer(text="Вы курите?", reply_markup=binary_keyboard)
    await QuestionnaireStates.rooms_number_question.set()


@dp.message_handler(lambda msg: msg.text in ["Да", "Нет"], state=QuestionnaireStates.rooms_number_question)
async def rooms_question(msg: types.Message, state: FSMContext):
    await state.update_data(smoking=msg.text)
    await msg.answer(text="Желаемое количество комнат?", reply_markup=room_num_keyboard)
    await QuestionnaireStates.about_question.set()


@dp.message_handler(lambda msg: msg.text in ["1-2", "2-3", "3-4", "Не важно"], state=QuestionnaireStates.about_question)
async def about_question(msg: types.Message, state: FSMContext):
    await state.update_data(rooms_number=str(msg.text))
    await msg.answer(text="Расскажите немного о себе, чтобы дать потенциальному соседу больше информации", reply_markup=types.ReplyKeyboardRemove())
    await QuestionnaireStates.photo_question.set()


@dp.message_handler(state=QuestionnaireStates.photo_question)
async def photo_question(msg: types.Message, state: FSMContext):
    await state.update_data(about=msg.text[:799])
    await msg.answer(text="Отлично, для завершения заполнения анкеты отправьте мне вашу фотографию", reply_markup=types.ReplyKeyboardRemove())
    await QuestionnaireStates.end_of_questionnaire.set()


@dp.message_handler(content_types=["photo"], state=QuestionnaireStates.end_of_questionnaire)
async def end_of_questionnaire(msg: types.Message, state: FSMContext):
    await state.update_data(photo=msg.photo[-1].file_id)
    data = await state.get_data()
    db.add_user(msg.from_user.id, data.get("name"), int(data.get("age")), data.get("gender"),
                data.get("roommate_gender"), (lambda: 1 if data.get("smoking") == "Да" else 0)(),
                data.get("rooms_number"), data.get("about"),
                data.get("photo"))
    await msg.answer(text="Ваша анкета успешно добавлена в базу! Теперь вы можете поискать соседа, удачи в поисках!",
                     reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
