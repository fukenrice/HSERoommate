from aiogram.dispatcher.filters.state import StatesGroup, State


class ModeratorStates(StatesGroup):
    moderating = State()
