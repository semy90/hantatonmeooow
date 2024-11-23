from aiogram import F, Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states.authorization import AuthorizationState
from src.bot.keyboards.main_funcs import not_authorization_keyboard, authorization_keyboard
from src.database.gateway import Database
from src.database.models.user import UserModel
from bot.filters.registred import AuthorizationFilter, NotAuthorizationFilter

autoriz_router = Router(name=__name__)


# кнопка отмены
@autoriz_router.message(F.text == "Авторизоваться", NotAuthorizationFilter(), StateFilter(None))
async def autoriz_handler(message: Message, session: AsyncSession, state: FSMContext):


    await message.answer("Введите e-mail:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(AuthorizationState.waiting_email)


@autoriz_router.message(AuthorizationState.waiting_email)
async def auto_waiting_email(message: Message, state: FSMContext):
    await state.update_data(e_mail=message.text.lower())

    await message.answer("Отлично, теперь пришлите пароль: ")
    await state.set_state(AuthorizationState.waiting_password)


@autoriz_router.message(AuthorizationState.waiting_password)
async def auto_waiting_email(message: Message, state: FSMContext):
    await state.update_data(password=message.text.lower())
    await message.answer("Пароль принят!")
    data = await state.get_data()
    kb = [
        [InlineKeyboardButton(text="Да", callback_data='yes_autoriz')],
        [InlineKeyboardButton(text="Нет", callback_data='no_autoriz')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer(
        f"Перепроверьте ваши данные\nemail: {data.get("e_mail")}\npassword: ||{data.get("password")}||\n\nВсе верно?",
        parse_mode='MarkdownV2', reply_markup=keyboard)
    await state.set_state(AuthorizationState.confirm_state)


@autoriz_router.callback_query(AuthorizationState.confirm_state, F.data == 'yes_autoriz')
async def answer(call: CallbackQuery, state: FSMContext,session : AsyncSession):
    #тут будет осуществляться запрос есть ли такой пользователь или нет
    database = Database(session)
    await database.change_authorizion(call)
    await state.clear()
    await call.message.answer("Вы успешно зарегистрировались!\nДля продолжения прожмите /start")


@autoriz_router.callback_query(AuthorizationState.confirm_state, F.data == 'no_autoriz')
async def answer(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer("Отменяю...")