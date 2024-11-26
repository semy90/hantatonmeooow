from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def not_authorization_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Авторизоваться")],
        [KeyboardButton(text="Зарегистрироваться")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard= True)
    return keyboard

def authorization_keyboard() -> InlineKeyboardMarkup:
    kb = [
        [InlineKeyboardButton(text="Поиск конфиренции", callback_data= 'search_conf'), InlineKeyboardButton(text="Ваш профиль", callback_data="profile")],
        [InlineKeyboardButton(text="Ваши конфиренции"), InlineKeyboardButton(text="Настройки", callback_data="profile")]
    ]
    keyboard = InlineKeyboardMarkup(keyboard=kb, resize_keyboard= True)
    return keyboard