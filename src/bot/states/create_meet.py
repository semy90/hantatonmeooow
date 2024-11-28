from aiogram.fsm.state import StatesGroup, State


class CreateState(StatesGroup):
    waiting_data = State()
    confirm_state = State()
