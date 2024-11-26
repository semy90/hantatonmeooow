from aiogram import Dispatcher, Bot

from bot.handlers.authorization import include_autoriz_routers

from bot.handlers.main_funcs.start import start_router as start_router
from bot.handlers.registration.registration import reg_router


def include_routers(dp: Dispatcher):
    include_autoriz_routers(dp)
    dp.include_routers(reg_router)
    dp.include_routers(start_router)
