import asyncio
import datetime
import json
import pprint
import re

import aioschedule
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, ReplyKeyboardRemove, TelegramObject, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums.parse_mode import ParseMode
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.callback_data.meet import CreateCallbackData, NotificationCallbackData
from bot.filters.is_autorization import NotAuthorizationFilter
from bot.filters.is_creator_vcs import CreatorFilter
from bot.states.authorization import AuthorizationState
from bot.states.create_meet import CreateState
from bot.states.creating_newsletter import CreateNewsletterState
from request.Users import Auth, Meetings
from src.bot.keyboards.main_funcs import not_authorization_keyboard, authorization_keyboard
from src.database.gateway import Database
from src.database.models.user import UserModel
from utils.changer import change
from utils.data_parser import data_parser, meet_parser

create_router = Router(name=__name__)
link = ""
meet_data = ''


@create_router.callback_query(F.data == 'create_conf', CreatorFilter())
async def create_meet(query: CallbackQuery, state: FSMContext):
    await query.message.answer("""Для создания конференции отправьте данные в виде(вместо квадратных скобок и информации в них):
[Имя конференции]
[Нужен ли включенный микрофон?(да или нет)]
[Нужена ли включенная камера?(да или нет)]
[Нужен ли зал ожидания?(да или нет)]
[Количество участников(целое число)]
[Начало конференции (в формате ГГГГ-ММ-ДД ЧЧ:ММ)]
[Продолжительность конференции(в минутах)]
[Уведомление о начале конференции(в формате ГГГГ-ММ-ДД ЧЧ:ММ)]
""")
    await state.set_state(CreateState.waiting_data)


@create_router.message(CreateState.waiting_data)
async def send_data(message: Message, state: FSMContext):
    kb = [
        [InlineKeyboardButton(text="Да", callback_data='yes_create_conf')],
        [InlineKeyboardButton(text="Нет", callback_data='no_create_conf')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await state.update_data(dat=message.text)
    await message.answer("Данные получены, создать вкс?", reply_markup=keyboard)
    await state.set_state(CreateState.confirm_state)


@create_router.callback_query(CreateState.confirm_state, F.data == 'yes_create_conf')
async def confirm_sending(query: CallbackQuery, session: AsyncSession, state: FSMContext):
    global link, meet_data
    dat = await state.get_data()
    s = data_parser(dat['dat'])
    database = Database(session)
    user = await database.get_user(query)
    data_about_meet = await Meetings.create_meetings(user['token'], s['name'], s['isMicrophoneOn'], s['isVideoOn'],
                                                     s['isWaitingRoomEnabled'],
                                                     s['participantsCount'], s['startedAt'], s['durationx'],
                                                     s['sendNotificationsAt'],
                                                     s['state'])
    meet_data = s
    pprint.pprint(data_about_meet)
    if (type(data_about_meet) == int):
        await query.message.answer(f"Ошибка! Номер ошибки: {data_about_meet}")
    else:
        s = meet_parser(data_about_meet)
        link = data_about_meet['permalink']

        kb = [
            [InlineKeyboardButton(text="Ссылка на конференцию", url=data_about_meet['permalink'])],
            [InlineKeyboardButton(text="Открыть конференцию", web_app=WebAppInfo(url=data_about_meet['permalink']))],
            [InlineKeyboardButton(text="🔔Отправить уведомление", callback_data='notification')],

        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
        await query.message.answer(f"⚠Информация о конференции⚠\n{s}", reply_markup=keyboard, parse_mode='html')
    await state.clear()


@create_router.callback_query(CreateState.confirm_state, F.data == 'no_create_conf')
async def confirm_sending(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Отменяю...")
    await state.clear()


@create_router.callback_query(F.data == 'notification')
async def notification(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Пришлите время для уведомления!")
    await state.set_state(CreateNewsletterState.waiting_data)


@create_router.message(CreateNewsletterState.waiting_data)
async def nouf_send(message: Message, state: FSMContext):
    global link, meet_data
    ymd, hm = message.text.split(' ')

    dt = datetime.datetime(year=ymd.split('-')[0], month=ymd.split('-')[1], day=ymd.split('-')[2],
                           hour=hm.split(':')[0], minute=hm.split(':')[1], second=0)
    delta = (dt - datetime.datetime.now()).total_seconds()

    await asyncio.sleep(delta)
    info = str(await state.get_data())
    kb = [
        [InlineKeyboardButton(text="Ссылка на конференцию", url=link)],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(text=meet_data,reply_markup=keyboard, parse_mode="html")
