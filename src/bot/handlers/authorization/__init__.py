from aiogram import Dispatcher, Bot

from bot.handlers.authorization.authorization import autoriz_router
from bot.handlers.authorization.profile import profile_router
from bot.handlers.authorization.settings import settings_router


def include_autoriz_routers(dp: Dispatcher):
    dp.include_routers(autoriz_router)
    dp.include_routers(profile_router)
    dp.include_routers(settings_router)
