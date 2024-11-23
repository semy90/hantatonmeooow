from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from database.gateway import Database


class NotAuthorizationFilter(BaseFilter):
    async def __call__(self, event: TelegramObject, session: AsyncSession) -> bool:
        database = Database(session)
        return not (await database.check_authorizion(event))


class AuthorizationFilter(BaseFilter):
    async def __call__(self, event: TelegramObject, session: AsyncSession) -> bool:
        database = Database(session)
        return await database.check_authorizion(event)
