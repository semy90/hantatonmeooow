from datetime import datetime, date

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callback_data.page_factory import AllCallbackData, YourCallbackData
from bot.filters.is_autorization import NotAuthorizationFilter
from bot.states.authorization import AuthorizationState
from bot.states.meetings import MeetingState
from request.Users import Auth, Meetings
from src.bot.keyboards.main_funcs import not_authorization_keyboard, authorization_keyboard
from src.database.gateway import Database, VCSGateway
from src.database.models.user import UserModel
from utils.bcs_parser import bcs_parser
from utils.changer import change

all_bcs_router = Router(name=__name__)


@all_bcs_router.callback_query(F.data == "conf")
async def bcs(query: CallbackQuery):
    kb = [
        [InlineKeyboardButton(text="➕Создать конференцию", callback_data='create_conf')],
        [InlineKeyboardButton(text="📅Конференция по периоду", callback_data="search_conf")],
        [InlineKeyboardButton(text="🔙Назад", callback_data="auto_menu")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await query.message.edit_text("Выберите категорию:", reply_markup=keyboard)


@all_bcs_router.callback_query(F.data == "search_conf")
async def search_bcs(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Пришлите время НАЧАЛА периода в формате <ГГГГ-ММ-ДД>")
    await state.set_state(MeetingState.waiting_fromDate)


@all_bcs_router.message(MeetingState.waiting_fromDate)
async def search_bcs(message: Message, state: FSMContext):
    await state.update_data(fromData=change(message.text))
    await message.answer("Пришлите время КОНЦА периода в формате <ГГГГ-ММ-ДД>")
    await state.set_state(MeetingState.waiting_toDate)


@all_bcs_router.message(MeetingState.waiting_toDate)
async def search_bcs(message: Message, state: FSMContext):
    await state.update_data(toData=change(message.text))
    kb = [
        [KeyboardButton(text="Забранированные"),
         KeyboardButton(text="Отмененные")],
        [KeyboardButton(text="Начавшиеся"),
         KeyboardButton(text="Законченные")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите тип конференции", reply_markup=keyboard)
    await state.set_state(MeetingState.waiting_state)


@all_bcs_router.message(MeetingState.waiting_state)
async def search_bcs(message: Message, session: AsyncSession, state: FSMContext):
    kb = [[InlineKeyboardButton(text="Продолжить", callback_data=AllCallbackData(page=0).pack())],
          [InlineKeyboardButton(text="Отмена", callback_data='cancel_meet')]]

    vcs = VCSGateway(session)
    await vcs.delete(message)

    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    f = False
    if change(message.text) == 'Забранированные':
        await state.update_data(state='booked')
        f = True
    elif change(message.text) == 'Отмененные':
        await state.update_data(state='cancelled')
        f = True
    elif change(message.text) == 'Начавшиеся':
        await state.update_data(state='started')
        f = True
    elif change(message.text) == 'Законченные':
        await state.update_data(state='ended')
        f = True
    else:
        await message.answer("Выберите что-то из панели")
        await state.set_state(MeetingState.waiting_state)

    if f:
        await message.answer("Ваши данные формируются для продолжения нажмите ниже", reply_markup=keyboard)
        await state.set_state(MeetingState.confirm)


@all_bcs_router.callback_query(AllCallbackData.filter(), MeetingState.confirm)
async def all_bcs(query: CallbackQuery, session: AsyncSession, state: FSMContext, callback_data: AllCallbackData):
    database = Database(session)
    vcs = VCSGateway(session)

    user = await database.get_user(query)
    data = await state.get_data()
    D1 = str(datetime(year=int(data["fromData"].split('-')[0]),
                      month=int(data["fromData"].split('-')[1]),
                      day=int(data["fromData"].split('-')[2])))
    D2 = str(datetime(year=int(data["toData"].split('-')[0]),
                      month=int(data["toData"].split('-')[1]),
                      day=int(data["toData"].split('-')[2])))
    d1 = 'T'.join(D1.split())
    d2 = 'T'.join(D2.split())

    meets = await vcs.get(query)
    if meets is "":
        tmp = await Meetings.meetings(user['token'], d1, d2)
        await vcs.put(query, tmp)
        meets = tmp

    count_bcs = len(meets)
    cur = int(str(callback_data).split('=')[1])
    if count_bcs == 0:
        await query.message.edit_text("Нет конференций!")
        return

    if cur < 0:
        cur = count_bcs - 1
    if cur > count_bcs - 1:
        cur = 0

    curbcs = meets[cur]
    cur_bcs = bcs_parser(curbcs)
    kb_bulder = InlineKeyboardBuilder()
    kb_bulder.row(InlineKeyboardButton(text=f"🔗Подключиться к конференции", url=curbcs['permalink']))
    kb_bulder.row(InlineKeyboardButton(text="<-", callback_data=AllCallbackData(page=cur - 1).pack()))
    kb_bulder.add(InlineKeyboardButton(text=f"{cur + 1}/{count_bcs}", callback_data='None'))
    kb_bulder.add(InlineKeyboardButton(text="->", callback_data=AllCallbackData(page=cur + 1).pack()))
    kb_bulder.row(InlineKeyboardButton(text="🔙Назад", callback_data='auto_menu'))
    kb_bulder.row(InlineKeyboardButton(text="🖥Открыть конференцию", web_app=WebAppInfo(url=curbcs['permalink'])))

    await query.message.edit_text(
        f"<b>Вся информация о конференции</b>:\n{cur_bcs}"
        , reply_markup=kb_bulder.as_markup())
