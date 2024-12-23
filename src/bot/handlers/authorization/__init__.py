from aiogram import Dispatcher, Bot

from bot.handlers.authorization.authorization import autoriz_router
from bot.handlers.authorization.create_meeting import create_router
from bot.handlers.authorization.profile import profile_router
from bot.handlers.authorization.settings import settings_router
from bot.handlers.authorization.work_with_bcs import all_bcs_router


def include_autoriz_routers(dp: Dispatcher):
    dp.include_routers(autoriz_router)
    dp.include_routers(profile_router)
    dp.include_routers(settings_router)
    dp.include_routers(all_bcs_router)
    dp.include_routers(create_router)
