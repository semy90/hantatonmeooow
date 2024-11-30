from aiogram.filters.callback_data import CallbackData


class CreateCallbackData(CallbackData, prefix='confirm='):
    page:str


class NotificationCallbackData(CallbackData, prefix='nouf='):
    page: str
