from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from database.gateway import Database
from request.Users import Account


class CreatorFilter(BaseFilter):
    async def __call__(self, event: TelegramObject, session: AsyncSession) -> bool:
        database = Database(session)
        user = await database.get_user(event)
        acc = (await Account().info(user['token']))['roles'][0]["permissions"]
        return "meeting.create" in acc
