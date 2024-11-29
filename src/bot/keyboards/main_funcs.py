from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.callback_data.page_factory import AllCallbackData


def not_authorization_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Авторизоваться")],
        [KeyboardButton(text="Зарегистрироваться")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def authorization_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="👤Ваш профиль", callback_data="profile")],
        [InlineKeyboardButton(text="🎦Конференции", callback_data="conf")],
        [InlineKeyboardButton(text="⚙Настройки", callback_data="settings")],
        [InlineKeyboardButton(text="🖥Открыть сайт",web_app= WebAppInfo(url='https://test.vcc.uriit.ru/meeting/'))],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard
