from aiogram.fsm.state import StatesGroup, State


class MeetingState(StatesGroup):
    waiting_fromDate = State()
    waiting_toDate = State()
    waiting_state = State()
    confirm = State()