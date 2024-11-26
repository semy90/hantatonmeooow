from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callback_data.page_factory import PageCallbackData
from bot.filters.is_autorization import NotAuthorizationFilter
from bot.states.authorization import AuthorizationState
from request.Users import Auth
from src.bot.keyboards.main_funcs import not_authorization_keyboard, authorization_keyboard
from src.database.gateway import Database
from src.database.models.user import UserModel
from utils.changer import change

all_bcs_router = Router(name=__name__)


@all_bcs_router.callback_query(PageCallbackData.filter())
async def all_bcs_router(query: CallbackQuery, callback_data: PageCallbackData):
    cur = int(str(callback_data).split('=')[1])

    # все конфы
    l = ['1','2','3']

    count_bcs = len(l)

    if count_bcs == 0:
        await query.message.edit_text("Нет обращений!")
        return

    if cur < 0:
        cur =count_bcs-1
    if cur > count_bcs:
        cur = 0

    cur_bcs = l[cur]


    kb_bulder = InlineKeyboardBuilder()
    kb_bulder.add(InlineKeyboardButton(text="<-", callback_data=PageCallbackData(page=cur - 1).pack()))
    kb_bulder.add(InlineKeyboardButton(text=f"{cur}/{count_bcs}", callback_data='None'))
    kb_bulder.add(InlineKeyboardButton(text="->", callback_data=PageCallbackData(page=cur + 1).pack()))
    kb_bulder.row(InlineKeyboardButton(text="Назад", callback_data='auto_menu'))


    await query.message.edit_text(
        f"Вся информация о конференции:\n{cur_bcs}"
        , reply_markup=kb_bulder.as_markup())
