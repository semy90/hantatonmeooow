import pprint
import re
from aiogram import F, Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums.parse_mode import ParseMode
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.is_autorization import NotAuthorizationFilter
from bot.filters.is_creator_vcs import CreatorFilter
from bot.states.authorization import AuthorizationState
from bot.states.create_meet import CreateState
from request.Users import Auth, Meetings
from src.bot.keyboards.main_funcs import not_authorization_keyboard, authorization_keyboard
from src.database.gateway import Database
from src.database.models.user import UserModel
from utils.changer import change
from utils.data_parser import data_parser

create_router = Router(name=__name__)


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
    dat = await state.get_data()
    s = data_parser(dat['dat'])
    database = Database(session)
    user = await database.get_user(query)
    await Meetings.create_meetings(user['token'], s['name'], s['isMicrophoneOn'], s['isVideoOn'],
                                   s['isWaitingRoomEnabled'],
                                   s['participantsCount'], s['startedAt'], s['durationx'], s['sendNotificationsAt'],
                                   s['state'])
    await query.message.answer("ВКС создана!")
    await state.clear()


@create_router.callback_query(CreateState.confirm_state, F.data == 'no_create_conf')
async def confirm_sending(query: CallbackQuery, state: FSMContext):
    await query.message.answer("Отменяю...")
    await state.clear()
