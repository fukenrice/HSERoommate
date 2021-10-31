from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from models.questionnaire import Questionnaire
from keyboards.default import scrolling_keyboard
from loader import dp, bot, db
from states.general_states import GeneralStates


async def show_next(user_questionnaire: Questionnaire, search_id: int, msg: types.message, state: FSMContext):
    # Есть ли вообще записи в таблице
    if db.questionnaire_in_table(search_id=0, roommate_gender=user_questionnaire.roommate_gender):
        # Если есть след запись
        if db.questionnaire_in_table(search_id=search_id, roommate_gender=user_questionnaire.roommate_gender):
            roommate_questionnaire = Questionnaire(
                db.get_next_questionnaire_by_search_id(search_id, user_questionnaire.roommate_gender))
            await msg.answer_photo(photo=roommate_questionnaire.photo, caption=f"{roommate_questionnaire.name}\n"
                                                                               f"Пол: {roommate_questionnaire.gender}\n"
                                                                               f"{roommate_questionnaire}\n",
                                   reply_markup=scrolling_keyboard)
            async with state.proxy() as data:
                data["current_id"] = roommate_questionnaire.id + 1
        # Показываем первую, запускаем второй круг
        else:
            search_id = 0
            roommate_questionnaire = Questionnaire(
                db.get_next_questionnaire_by_search_id(search_id, user_questionnaire.roommate_gender))
            async with state.proxy() as data:
                data["current_id"] = roommate_questionnaire.id + 1
            await msg.answer_photo(photo=roommate_questionnaire.photo, caption=f"{roommate_questionnaire.name}\n"
                                                                               f"Пол: {roommate_questionnaire.gender}\n"
                                                                               f"{roommate_questionnaire}\n",
                                   reply_markup=scrolling_keyboard)
    # Записей, подходящих под условие нет совсем
    else:
        await msg.answer(
            text="В нашей базе пока нет анкет, подходящих под ваши фильтры, попробуйте поменять пол соседа или "
                 "дождаться появления анкеты с нужными критериями")
        await state.finish()


@dp.message_handler(Command("show"), state="*")
async def start_polling(msg: types.Message, state: FSMContext):
    await GeneralStates.questionnaire_searching.set()
    # Если нету анкеты самого пользователя в бд.
    if not db.questionnaire_in_table(telegram_id=msg.from_user.id):
        await msg.answer(
            text="Для просмотра чужих анкет, пожалуйста, сначала добавьте свою при помощи команды /new_questionnaire")
        await state.finish()
    else:
        # Получение анкеты пользователя из бд для параметров поиска.
        user_questionnaire = Questionnaire(db.get_questionnaire_by_urser_id(msg.from_user.id))
        async with state.proxy() as data:
            data["roommate_gender"] = user_questionnaire.roommate_gender
            try:
                search_id = data["current_id"]
            except KeyError as e:
                search_id = 0
                data["current_id"] = 0
        await show_next(user_questionnaire, search_id, msg, state)


@dp.message_handler(lambda message: (message.text == "\N{THUMBS DOWN SIGN}"),
                    state=GeneralStates.questionnaire_searching)
async def continue_scrolling_negative(msg: types.Message, state: FSMContext):
    user_questionnaire = Questionnaire(db.get_questionnaire_by_urser_id(msg.from_user.id))
    async with state.proxy() as data:
        search_id = data["current_id"]
    await show_next(user_questionnaire, search_id, msg, state)


@dp.message_handler(lambda message: (message.text == "\N{THUMBS UP SIGN}"), state=GeneralStates.questionnaire_searching)
async def continue_scrolling_posititve(msg: types.Message, state: FSMContext):
    # Отправим пользователю, которого лвйкнули сообщение.
    async with state.proxy() as data:
        search_id = data["current_id"]
    user_questionnaire = Questionnaire(db.get_questionnaire_by_urser_id(msg.from_user.id))
    liked = db.questionnaire_by_search_id(search_id - 1)
    if liked is not None:
        other_questionnaire = Questionnaire(liked)

        await bot.send_photo(chat_id=other_questionnaire.telegram_id, photo=user_questionnaire.photo,
                                                                       caption=f"Ваша анкта понравилась человеку:\n"
                                                                       f"{user_questionnaire.name}\n"
                                                                       f"Пол: {user_questionnaire.gender}\n"
                                                                       f"{user_questionnaire}\n"
                                                                       f"Вот его ник тг: @{msg.from_user.username}")

    await show_next(user_questionnaire, search_id, msg, state)


@dp.message_handler(lambda message: message.text == "\N{Octagonal Sign}", state=GeneralStates.questionnaire_searching)
async def stop_scrolling(msg: types.Message, state: FSMContext):
    await msg.answer(text="Надеемся, вы кого-нибудь нашли, ждем вас снова)", reply_markup=types.ReplyKeyboardRemove())
    await GeneralStates.main_menu.set()
