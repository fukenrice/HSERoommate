from aiogram.dispatcher.filters.state import StatesGroup, State


class GeneralStates(StatesGroup):
    main_menu = State()
    questionnaire_edit = State()
    questionnaire_editing_field = State()
    edited_gender = State()
    edited_roommate_gender = State()
    edited_name = State()
    edited_age = State()
    edited_smoking = State()
    edited_about = State()
    edited_photo = State()

