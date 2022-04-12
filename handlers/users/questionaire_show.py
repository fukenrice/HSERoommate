from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import scrolling_keyboard, main_keyboard
from loader import dp, bot, db
from models.questionnaire import Questionnaire
from states.general_states import GeneralStates


async def send_questionnaire(msg: types.Message, roommate_questionnaire: Questionnaire, state: FSMContext):
    await msg.answer_photo(photo=roommate_questionnaire.photo, caption=f"{roommate_questionnaire}\n",
                           reply_markup=scrolling_keyboard)
    async with state.proxy() as data:
        data["current_id"] = roommate_questionnaire.id + 1


async def show_next(user_questionnaire: Questionnaire, search_id: int, msg: types.message, state: FSMContext):
    # Есть ли вообще записи в таблице
    if db.questionnaire_in_table(search_id=0, roommate_gender=user_questionnaire.roommate_gender,
                                 telegram_id=user_questionnaire.telegram_id, user_gender=user_questionnaire.gender):
        # Если есть след запись
        if db.questionnaire_in_table(search_id=search_id, roommate_gender=user_questionnaire.roommate_gender,
                                     telegram_id=user_questionnaire.telegram_id, user_gender=user_questionnaire.gender):
            roommate_questionnaire = Questionnaire(
                db.get_next_questionnaire_by_search_id(search_id, user_questionnaire.roommate_gender,
                                                       ignore_tg_id=user_questionnaire.telegram_id, user_gender=user_questionnaire.gender))
            await send_questionnaire(msg, roommate_questionnaire, state)
        # Показываем первую, запускаем второй круг
        else:
            search_id = 0
            roommate_questionnaire = Questionnaire(
                db.get_next_questionnaire_by_search_id(search_id, user_questionnaire.roommate_gender,
                                                       ignore_tg_id=user_questionnaire.telegram_id, user_gender=user_questionnaire.gender))
            await send_questionnaire(msg, roommate_questionnaire, state)
    # Записей, подходящих под условие нет совсем
    else:
        await msg.answer(
            text="В нашей базе пока нет анкет, подходящих под ваши фильтры, попробуйте поменять пол соседа или "
                 "дождаться появления анкеты с нужными критериями", reply_markup=main_keyboard)
        await state.finish()


@dp.message_handler(lambda msg: msg.text in ["/show", "Посмотреть анкеты"], state="*")
async def start_scrolling(msg: types.Message, state: FSMContext):
    await GeneralStates.questionnaire_searching.set()
    # Если нету анкеты самого пользователя в бд.
    if not db.questionnaire_in_table(telegram_id=msg.from_user.id):
        await msg.answer(
            text="Для просмотра чужих анкет, пожалуйста, сначала добавьте свою при помощи команды /new_form",
            reply_markup=main_keyboard)
        await state.finish()
    else:
        # Получение анкеты пользователя из бд для параметров поиска.
        user_questionnaire = Questionnaire(db.get_questionnaire_by_user_id(msg.from_user.id))
        async with state.proxy() as data:
            data["roommate_gender"] = user_questionnaire.roommate_gender
            try:
                search_id = data["current_id"]
            except KeyError as e:
                search_id = 0
                data["current_id"] = 0
        await show_next(user_questionnaire, search_id, msg, state)


@dp.message_handler(lambda message: message.text in ["\N{THUMBS DOWN SIGN}", "\N{Squared Sos} Пожаловаться"],
                    state=GeneralStates.questionnaire_searching)
async def continue_scrolling_negative(msg: types.Message, state: FSMContext):
    if msg.text == "\N{Squared Sos} Пожаловаться":
        async with state.proxy() as data:
            search_id = data["current_id"]
        reported = Questionnaire(db.questionnaire_by_search_id(search_id - 1))

        if reported is not None:
            db.add_reported(reported.telegram_id)

    user_questionnaire = Questionnaire(db.get_questionnaire_by_user_id(msg.from_user.id))
    async with state.proxy() as data:
        search_id = data["current_id"]
    await show_next(user_questionnaire, search_id, msg, state)


@dp.message_handler(lambda message: (message.text == "\N{THUMBS UP SIGN}"), state=GeneralStates.questionnaire_searching)
async def continue_scrolling_posititve(msg: types.Message, state: FSMContext):
    # Отправим пользователю, которого лвйкнули сообщение.
    async with state.proxy() as data:
        search_id = data["current_id"]
    user_questionnaire = Questionnaire(db.get_questionnaire_by_user_id(msg.from_user.id))
    liked = db.questionnaire_by_search_id(search_id - 1)
    if liked is not None:
        other_questionnaire = Questionnaire(liked)
        db.add_like(user_questionnaire.telegram_id, other_questionnaire.telegram_id)
        try:
            await bot.send_photo(chat_id=other_questionnaire.telegram_id, photo=user_questionnaire.photo,
                                 caption=f"Ваша анкета понравилась человеку:\n"
                                         f"{user_questionnaire}\n"
                                         f"Вот его ник тг: @{msg.from_user.username}")
        except Exception:
            pass  # Можно добавить удаление из бд и сообщение ищущему, что пользователь перестал пользоваться сервисом.

    await show_next(user_questionnaire, search_id, msg, state)


@dp.message_handler(lambda message: message.text == "\N{Octagonal Sign} Остановить поиск", state=GeneralStates.questionnaire_searching)
async def stop_scrolling(msg: types.Message, state: FSMContext):
    await msg.answer(text="Надеемся, вы кого-нибудь нашли, ждем вас снова)", reply_markup=main_keyboard)
    await GeneralStates.main_menu.set()
