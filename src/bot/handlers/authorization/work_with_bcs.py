import asyncio
import pprint
import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callback_data.meet import NotificationCallbackData
from bot.callback_data.page_factory import AllCallbackData, YourCallbackData
from bot.filters.is_autorization import NotAuthorizationFilter
from bot.states.authorization import AuthorizationState
from bot.states.creating_newsletter import CreateNewsletterState
from bot.states.meetings import MeetingState
from request.Users import Auth, Meetings
from src.bot.keyboards.main_funcs import not_authorization_keyboard, authorization_keyboard
from src.database.gateway import Database, VCSGateway
from src.database.models.user import UserModel
from utils.bcs_parser import bcs_parser
from utils.changer import change
from utils.data_parser import meet_parser, meet_parser1

all_bcs_router = Router(name=__name__)
link1 = ''
meet_data1 = ''


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
        await message.answer("Ваши данные формируются для продолжения нажмите ниже", keyboard=ReplyKeyboardRemove(),
                             reply_markup=keyboard)
        await state.set_state(MeetingState.confirm)


@all_bcs_router.callback_query(AllCallbackData.filter(), MeetingState.confirm)
async def all_bcs(query: CallbackQuery, session: AsyncSession, state: FSMContext, callback_data: AllCallbackData):
    global meet_data1,link1
    database = Database(session)
    vcs = VCSGateway(session)

    user = await database.get_user(query)
    data = await state.get_data()
    D1 = str(datetime.datetime (year=int(data["fromData"].split('-')[0]),
                      month=int(data["fromData"].split('-')[1]),
                      day=int(data["fromData"].split('-')[2])))
    D2 = str(datetime.datetime(year=int(data["toData"].split('-')[0]),
                      month=int(data["toData"].split('-')[1]),
                      day=int(data["toData"].split('-')[2])))
    d1 = 'T'.join(D1.split())
    d2 = 'T'.join(D2.split())

    meets = await vcs.get(query)
    if meets == "":
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

    # cur_bcs = bcs_parser(curbcs)
    cur_bcs = meet_parser1(curbcs)

    kb = [
        [InlineKeyboardButton(text="⏪", callback_data=AllCallbackData(page=cur - 1).pack()),
         InlineKeyboardButton(text=f"{cur + 1}/{count_bcs}", callback_data='None'),
         InlineKeyboardButton(text="⏩", callback_data=AllCallbackData(page=cur + 1).pack())],
        [InlineKeyboardButton(text=f"🔗Подключиться к конференции", url=curbcs['permalink'])],
        [InlineKeyboardButton(text="🖥Открыть конференцию", web_app=WebAppInfo(url=curbcs['permalink']))],
        [InlineKeyboardButton(text="🔔Создать уведомление", callback_data="ni_noutification")],
        [InlineKeyboardButton(text="🔙Назад", callback_data='auto_menu')]

    ]
    link1 = curbcs['permalink']
    meet_data1 = cur_bcs
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await query.message.edit_text(
        f"<b>Вся информация о конференции</b>:\n{cur_bcs}"
        , reply_markup=keyboard, parse_mode='html')


@all_bcs_router.callback_query(F.data == 'ni_noutification')
async def notification(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Пришлите время для уведомления!")
    await state.set_state(CreateNewsletterState.waiting_data)


@all_bcs_router.message(CreateNewsletterState.waiting_data)
async def nouf_send(message: Message, state: FSMContext):
    global link1, meet_data1
    ymd, hm = message.text.split(' ')

    dt = datetime.datetime(year=int(ymd.split('-')[0]), month=int(ymd.split('-')[1]), day=int(ymd.split('-')[2]),
                           hour=int(hm.split(':')[0]), minute=int(hm.split(':')[1]), second=0)
    delta = (dt - datetime.datetime.now()).total_seconds()

    info = str(await state.get_data())
    await asyncio.sleep(delta)
    kb = [
        [InlineKeyboardButton(text="Ссылка на конференцию", url=link1)],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(text=meet_data1, reply_markup=keyboard,parse_mode="html")
