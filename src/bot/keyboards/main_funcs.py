from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def not_authorization_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Авторизоваться")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard= True)
    return keyboard

def authorization_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Поиск конфиренции"), KeyboardButton(text="Ваш профиль")],
        [KeyboardButton(text="Ваши конфиренции"), KeyboardButton(text="Настройки")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard= True)
    return keyboard