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

autoriz_router = Router(name=__name__)


# кнопка отмены
@autoriz_router.message(F.text == "Авторизоваться", NotAuthorizationFilter(), StateFilter(None))
async def autoriz_handler(message: Message, state: FSMContext):
    await message.answer("Введите логин: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AuthorizationState.waiting_login)


@autoriz_router.message(AuthorizationState.waiting_login)
async def auto_waiting_email(message: Message, state: FSMContext):
    await state.update_data(login=change(message.text))

    await message.answer("Отлично, теперь пришлите пароль: ")
    await state.set_state(AuthorizationState.waiting_password)


@autoriz_router.message(AuthorizationState.waiting_password)
async def auto_waiting_email(message: Message, state: FSMContext):
    await state.update_data(password=change(message.text))
    await message.answer("Пароль принят!")
    data = await state.get_data()
    kb = [
        [InlineKeyboardButton(text="Да", callback_data='yes_autoriz')],
        [InlineKeyboardButton(text="Нет", callback_data='no_autoriz')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(
        f"Перепроверьте ваши данные\nlogin: {data.get("login")}\npassword: {data.get("password")}\n\nВсе верно?",
         reply_markup=keyboard)
    await state.set_state(AuthorizationState.confirm_state)


@autoriz_router.callback_query(AuthorizationState.confirm_state, F.data == 'yes_autoriz')
async def answer(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    res = await Auth().login(data.get("login"), data.get("password"))

    if type(res) == int:
        await call.message.answer("Ошибка в логине или в пароле")
    else:
        database = Database(session)
        await database.change_token_with_id(call, res)
        await call.message.answer("Вы успешно авторизовались!\nДля продолжения прожмите /start")
    await state.clear()


@autoriz_router.callback_query(AuthorizationState.confirm_state, F.data == 'no_autoriz')
async def answer(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer("Отменяю...")
