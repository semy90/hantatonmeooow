from aiogram.fsm.state import StatesGroup, State


class CreateNewsletterState(StatesGroup):
    waiting_data = State()