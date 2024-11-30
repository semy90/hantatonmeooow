import asyncio
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
from bot.states.datastate import UserNameState
from request.Users import Auth, Account
from src.bot.keyboards.main_funcs import not_authorization_keyboard, authorization_keyboard
from src.database.gateway import Database
from src.database.models.user import UserModel
from utils.changer import change
from utils.data_sender import data_sender, data_for_change_name

profile_router = Router(name=__name__)


@profile_router.callback_query(F.data == "profile")
async def profile_user(query: CallbackQuery, session: AsyncSession):
    database = Database(session)
    user = await database.get_user(query)
    data = await Account.info(user['token'])
    kb = [
        [InlineKeyboardButton(text="🔄Изменить ФИО", callback_data='change_name'),
         InlineKeyboardButton(text="🔄Изменить почту✉", callback_data='change_email')],
        [InlineKeyboardButton(text="🔄Изменить телефон☎", callback_data='phone')],
        [InlineKeyboardButton(text="🔙Назад", callback_data="auto_menu")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    s = data_sender(data)
    await query.message.edit_text(text=s, reply_markup=keyboard,parse_mode='html')


@profile_router.callback_query(F.data == 'change_name')
async def change_firstname(query: CallbackQuery, state: FSMContext):
    kb = [[KeyboardButton(text="Оставить текущее")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await query.message.answer("Пришлите новое <b>имя</b> пользователя!", reply_markup=keyboard,parse_mode="html")
    await state.set_state(UserNameState.waiting_firstname)


@profile_router.message(UserNameState.waiting_firstname)
async def change_lastname(message: Message, state: FSMContext):
    if message.text == "Оставить текущее":
        await state.update_data(firstname=None)
    else:
        await state.update_data(firstname=change(message.text))
    kb = [[KeyboardButton(text="Оставить текущее")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await state.set_state(UserNameState.waiting_lastname)
    await message.answer("Пришлите новую <b>фамилию</b> пользователя!", reply_markup=keyboard,parse_mode="html")


@profile_router.message(UserNameState.waiting_lastname)
async def change_lastname(message: Message, state: FSMContext):
    if message.text == "Оставить текущее":
        await state.update_data(lastname=None)
    else:
        await state.update_data(lastname=change(message.text))
    kb = [[KeyboardButton(text="Оставить текущее")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await state.set_state(UserNameState.waiting_middlename)
    await message.answer("Пришлите новое <b><отчество</b> пользователя!", reply_markup=keyboard,parse_mode="html")


@profile_router.message(UserNameState.waiting_middlename)
async def change_middlename(message: Message, state: FSMContext):
    if message.text == "Оставить текущее":
        await state.update_data(middlename=None)
    else:
        await state.update_data(middlename=change(message.text))
    await state.set_state(UserNameState.confirm_state)

    data = await state.get_data()

    kb = [
        [InlineKeyboardButton(text="Да", callback_data='yes_change_name')],
        [InlineKeyboardButton(text="Нет", callback_data='no_change_name')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)

    s = data_for_change_name(data)
    if s == '':
        await message.answer("Изменений нет❗",keyboard=ReplyKeyboardRemove())
        await state.clear()
    else:
        await state.set_state(UserNameState.confirm_state)
        await message.answer(f"Подтвердить изменения:\n{s}",keyboard=ReplyKeyboardRemove(), reply_markup=keyboard)


@profile_router.callback_query(UserNameState.confirm_state, F.data == "yes_change_name")
async def confirm_changes(query: CallbackQuery, session: AsyncSession, state : FSMContext):
    database = Database(session)
    user = await database.get_user(query)
    data = await state.get_data()
    await Account.refact_info(user["token"], last_name= data.get('lastname'), first_name=data.get('firstname'),middle_name=data.get("middlename", ))
    await state.clear()

@profile_router.callback_query(UserNameState.confirm_state, F.data == "no_change_name")
async def confirm_changes(query: CallbackQuery, session: AsyncSession, state : FSMContext):
    await query.message.answer("Отменяю!")
    await state.clear()
