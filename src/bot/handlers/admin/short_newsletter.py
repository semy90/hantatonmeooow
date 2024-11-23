import asyncio

from aiogram import Bot, Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.filters import AdminFilter
from database.gateway import Database

short_newsletter_router = Router(name=__name__)


@short_newsletter_router.message(AdminFilter(), F.text.startswith("/message"))
async def short_message(message: Message, session: AsyncSession, bot: Bot):
    _, *tmp = message.text.split()
    text = ' '.join(tmp)
    if text == '':
        await message.reply('Пустое сообщение!')

    base = Database(session)
    user_ids = await base.get_all_users()
    for uid in user_ids:
        await bot.send_message(chat_id=uid, text=text)
        await asyncio.sleep(0.05)

    await message.answer('Рассылка завершена!')
