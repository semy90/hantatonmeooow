import os
from types import NoneType
from typing import List

import sqlalchemy as sa
from aiogram.types import TelegramObject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.user import UserModel
from request.Users import Auth


class UserGateway:
    pass


class SubsGateway:
    pass


class Database:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, event: TelegramObject):
        query = sa.select(UserModel).where(UserModel.token == old_token)
        user = await self.session.scalar(query)
        tmp_dict = {
            'id': user.id,
            'name': user.name,
            'user_id': user.userid,
            'token': user.token,
        }
        return tmp_dict

    async def change_token_with_old_token(self, old_token: str, new_token: str):
        query = sa.select(UserModel).where(UserModel.token == old_token)
        user = await self.session.scalar(query)
        user.token = new_token
        # self.session.add(user)
        await self.session.commit()

    async def change_token_with_id(self, event: TelegramObject, data: dict):
        query = sa.select(UserModel).where(UserModel.id == event.from_user.id)
        user = await self.session.scalar(query)
        user.token = data["token"]
        user.userid = data["user"]['id']
        # self.session.add(user)
        await self.session.commit()

    async def check_authorizion(self, event: TelegramObject) -> bool:
        """Возвращает True если пользователь зарегистрирован"""

        query = sa.select(UserModel).where(UserModel.id == event.from_user.id)
        user = await self.session.scalar(query)
        return user.token != ''

    async def get_all_users(self) -> List[int]:
        query = sa.select(UserModel)
        users = await self.session.scalars(query)
        return [user.id for user in users]

    async def add_new_user(self, event: TelegramObject):
        stmt = select(UserModel).where(UserModel.id == event.from_user.id)
        user = await self.session.scalar(stmt)
        if user is None:
            user = UserModel(
                id=event.from_user.id,
                name=event.from_user.username,
                token="",
                userid=-1
            )
            self.session.add(user)

        if user.name != event.from_user.username:
            # Дополнительная проверка на смену ника у пользователя
            user.name = event.from_user.username
        await self.session.commit()
