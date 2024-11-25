from aiogram.fsm.state import StatesGroup, State


class AuthorizationState(StatesGroup):
    waiting_login = State()
    waiting_password = State()
    confirm_state = State()
