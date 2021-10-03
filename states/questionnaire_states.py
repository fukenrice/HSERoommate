from aiogram.dispatcher.filters.state import StatesGroup, State


class QuestionnaireStates(StatesGroup):
    name_question = State()
    age_question = State()
    gender_question = State()
    roommate_gender_question = State()
    smoking_question = State()
    rooms_number_question = State()
    about_question = State()
    photo_question = State()
    end_of_questionnaire = State()
