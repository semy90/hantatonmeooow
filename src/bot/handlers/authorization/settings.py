from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.is_autorization import NotAuthorizationFilter
from bot.states.authorization import AuthorizationState
from request.Users import Auth
from src.bot.keyboards.main_funcs import not_authorization_keyboard, authorization_keyboard
from src.database.gateway import Database
from src.database.models.user import UserModel
from utils.changer import change

settings_router = Router(name=__name__)


@settings_router.callback_query(F.data == "settings")
async def settings_user(query: CallbackQuery):
    kb = [
        [InlineKeyboardButton(text="🔔Настройка оповещений", callback_data='None'),
         InlineKeyboardButton(text="🔄Сменить пароль", callback_data='None')],
        [InlineKeyboardButton(text="🔚Выйти из аккаунта", callback_data="logout")],
        [InlineKeyboardButton(text="🔙Назад", callback_data="auto_menu")]

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await query.message.edit_text("⚙Настройки вашего аккаунта аккаунта:", reply_markup=keyboard)


@settings_router.callback_query(F.data == "logout")
async def logout(query: CallbackQuery, session: AsyncSession):
    database = Database(session)
    user = await database.get_user(query)
    await Auth.logout(user['token'])
    await database.delete_user(query)
    await query.message.answer("‼Вы вышли из аккаунта‼")