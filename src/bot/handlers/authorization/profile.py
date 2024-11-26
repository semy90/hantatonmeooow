import pprint
import re
from aiogram import F, Router
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

profile_router = Router(name=__name__)


@profile_router.callback_query(F.data == "profile")
async def profile_user(query: CallbackQuery, session: AsyncSession):
    kb = [
        [InlineKeyboardButton(text="Изменить ФИО", callback_data='None'),
         InlineKeyboardButton(text="Изменить почту", callback_data='None')],
        [InlineKeyboardButton(text="Как профиль видят другие?", callback_data="None")],
        [InlineKeyboardButton(text="Назад", callback_data="auto_menu")]

    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await query.message.edit_text("Вот ваш профиль: ", reply_markup=keyboard)
