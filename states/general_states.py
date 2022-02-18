from aiogram.dispatcher.filters.state import StatesGroup, State


class GeneralStates(StatesGroup):
    main_menu = State()
    questionnaire_edit = State()
    questionnaire_searching = State()
    questionnaire_editing_field = State()
    edited_gender = State()
    edited_roommate_gender = State()
    edited_name = State()
    edited_age = State()
    edited_how_long = State()
    edited_budget = State()
    edited_location_global = State()
    edited_location_local = State()
    edited_pet = State()
    edited_apartment = State()
    edited_smoking = State()
    edited_about = State()
    edited_photo = State()

