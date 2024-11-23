from aiogram import Dispatcher, Bot

from bot.handlers.authorization.authorization import autoriz_router
from bot.handlers.main_funcs.start import start_router as start_router
from bot.handlers.main_funcs.about import about_router


def include_routers(dp: Dispatcher):
    dp.include_routers(autoriz_router)
    dp.include_routers(about_router)
    dp.include_routers(start_router)
