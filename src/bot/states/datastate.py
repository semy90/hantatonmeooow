from aiogram.fsm.state import StatesGroup, State


class UserNameState(StatesGroup):
    waiting_firstname = State()
    waiting_lastname = State()
    waiting_middlename = State()
    confirm_state = State()

class EmailState(StatesGroup):
    waiting_email = State()
    confirm_state = State()

class PhoneState(StatesGroup):
    waiting_phone = State()
    confirm_state = State()