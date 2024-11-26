from aiogram.filters.callback_data import CallbackData


class AllCallbackData(CallbackData, prefix='to'):
    page: int

class YourCallbackData(CallbackData, prefix='yours_to'):
    page: int