from aiogram.dispatcher.filters.state import StatesGroup, State


class QuestionnaireStates(StatesGroup):
    name_question = State()
    age_question = State()
    gender_question = State()
    roommate_gender_question = State()
    smoking_question = State()
    how_long_question = State()
    budget_question = State()
    location_global_question = State()
    location_local_question = State()
    pet_question = State()
    apartment_question = State()
    rooms_number_question = State()
    about_question = State()
    photo_question = State()
    end_of_questionnaire = State()
