from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters.is_autorization import AuthorizationFilter, NotAuthorizationFilter
from src.bot.keyboards.main_funcs import not_authorization_keyboard, authorization_keyboard
from src.database.gateway import Database
from src.database.models.user import UserModel

start_router = Router(name=__name__)


# проверка на незарег пользователя
@start_router.message(CommandStart(), NotAuthorizationFilter() )
async def start_handler(message: Message):
    await message.answer('Приветствую вас в меню бота!\nДля продолжения работы в системе, пройдите авторизацию',
                         reply_markup=not_authorization_keyboard()
                         )


@start_router.message(CommandStart(), AuthorizationFilter())
async def start_handler(message: Message):
    await message.answer('Приветствую вас в меню бота!\nВот вся доступная информация на данный момент: ',
                         reply_markup=authorization_keyboard()
                         )
@start_router.callback_query(F.data == "auto_menu")
async def start_handler(message: Message):
    await message.answer('Приветствую вас в меню бота!\nВот вся доступная информация на данный момент: ',
                         reply_markup=authorization_keyboard()
                         )


@start_router.message()
async def i_dont_understand(message: Message):
    await message.reply("Я вас не понимаю!")




