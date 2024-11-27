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
from bot.states.registration import RegistrationState
from request.Users import Auth
from src.bot.keyboards.main_funcs import not_authorization_keyboard, authorization_keyboard
from src.database.gateway import Database
from src.database.models.user import UserModel
from utils.changer import change

reg_router = Router(name=__name__)


@reg_router.message(F.text == "Зарегистрироваться", NotAuthorizationFilter(),StateFilter(None))
async def reg_handler(message: Message, state: FSMContext):
    await message.answer("Введите логин: ", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationState.waiting_login)


@reg_router.message(RegistrationState.waiting_login)
async def reg_waiting_login(message: Message, state: FSMContext):
    await state.update_data(login=change(message.text))


    await message.answer("Отлично, теперь пришлите почту: ")
    await state.set_state(RegistrationState.waiting_email)


@reg_router.message(RegistrationState.waiting_email)
async def reg_waiting_email(message: Message, state: FSMContext):
    await state.update_data(email=change(message.text))

    await message.answer("Отлично, теперь пришлите пароль: ")
    await state.set_state(RegistrationState.waiting_password)


@reg_router.message(RegistrationState.waiting_password)
async def reg_waiting_password(message: Message, state: FSMContext):
    await state.update_data(password=change(message.text))

    await message.answer("Отлично, теперь пришлите вашу фамилию: ")
    await state.set_state(RegistrationState.waiting_lastname)


@reg_router.message(RegistrationState.waiting_lastname)
async def reg_waiting_lastname(message: Message, state: FSMContext):
    await state.update_data(lastname=change(message.text))

    await message.answer("Отлично, теперь пришлите ваше имя: ")
    await state.set_state(RegistrationState.waiting_firstname)


@reg_router.message(RegistrationState.waiting_firstname)
async def auto_waiting_firstname(message: Message, state: FSMContext):
    await state.update_data(firstname=change(message.text))

    await message.answer("Отлично, теперь пришлите ваше отчество: ")
    await state.set_state(RegistrationState.waiting_middlename)


@reg_router.message(RegistrationState.waiting_middlename)
async def reg_waiting_middlename(message: Message, state: FSMContext):
    await state.update_data(middlename=change(message.text))

    await message.answer("Отлично, теперь пришлите ваш номер: ")
    await state.set_state(RegistrationState.waiting_phone)


@reg_router.message(RegistrationState.waiting_phone)
async def reg_waiting_phone(message: Message, state: FSMContext):
    await state.update_data(phone=change(message.text))

    await message.answer("Отлично, теперь пришлите вашу дату рождение в формате <ДД-ММ-ГГГГ>")
    await state.set_state(RegistrationState.waiting_bithday)


@reg_router.message(RegistrationState.waiting_bithday)
async def reg_waiting_birthday(message: Message, state: FSMContext):
    await state.update_data(birthday=change(message.text))

    data = await state.get_data()
    kb = [
        [InlineKeyboardButton(text="Да", callback_data='yes_reg')],
        [InlineKeyboardButton(text="Нет", callback_data='no_reg')]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    await state.set_state(RegistrationState.confirm_state)
    await message.answer(
        f"Все верно?\nВот ваши данные:\nlogin:{data.get("login")}\nemail:{data.get("email")}\npassword:{data.get("password")}\nФамилия:{data.get("lastname")}\nИмя:{data.get("firstname")}\nОтчество:{data.get("middlename")}\nНомер телефона:{data.get("phone")}\nДата рождения:{data.get("birthday")}",
        reply_markup=keyboard
    )


@reg_router.callback_query(RegistrationState.confirm_state, F.data == "yes_reg")
async def reg_waiting_confirm(call:CallbackQuery, state: FSMContext):
    data = await state.get_data()
    res = await Auth().register(data.get("login"), data.get("password"),data.get("email"),data.get("lastname"), data.get("firstname"), data.get("middlename"), data.get("phone"), data.get("birthday"))

    if res == 201:
        await call.message.answer("Вы успешно зарегистрировались")

    else:
        await call.message.answer("Ошибка!")
    await state.clear()

@reg_router.callback_query(RegistrationState.confirm_state, F.data == 'no_reg')
async def answer(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer("Отменяю...")
