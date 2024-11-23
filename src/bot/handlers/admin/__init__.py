from aiogram import Dispatcher, Bot

from .add_admin import add_router
from .admin_handler import admin_router
from .del_admin import del_router

from .short_newsletter import short_newsletter_router


def include_admin_routers(dp: Dispatcher):
    dp.include_routers(admin_router)
    dp.include_routers(del_router)
    dp.include_routers(add_router)
    dp.include_routers(short_newsletter_router)