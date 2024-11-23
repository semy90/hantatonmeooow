from aiogram.fsm.state import StatesGroup, State


class AuthorizationState(StatesGroup):
    waiting_email = State()
    waiting_password = State()
    confirm_state = State()
