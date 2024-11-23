import os
from types import NoneType
from typing import List

import sqlalchemy as sa
from aiogram.types import TelegramObject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from database.models.user import UserModel


class UserGateway:
    pass


class SubsGateway:
    pass



class Database:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def change_authorizion(self, event: TelegramObject):
        stmt = select(UserModel).where(UserModel.id == event.from_user.id)
        user = await self.session.scalar(stmt)
        if user.is_registered:
            user.is_registered = False
        else:
            user.is_registered = True
        self.session.add(user)
        await self.session.commit()

    async def check_authorizion(self, event: TelegramObject):
        stmt = select(UserModel).where(UserModel.id == event.from_user.id)
        user = await self.session.scalar(stmt)
        return bool(user.is_registered)

    async def get_all_users(self) -> List[int]:
        query = sa.select(UserModel)
        users = await self.session.scalars(query)
        return [user.id for user in users]

    async def get_admins(self) -> List[int]:
        query = sa.select(UserModel).where(UserModel.is_admin == True)
        admins = await self.session.scalars(query)
        return [admin.id for admin in admins]

    async def make_new_admin(self, name: str) -> None:
        query = sa.select(UserModel).where(UserModel.name == name)
        user = await self.session.scalar(query)
        if isinstance(user, UserModel):
            user.is_admin = True
            await self.session.commit()

    async def del_admin(self, name: str) -> None:
        query = sa.select(UserModel).where(UserModel.name == name)
        user = await self.session.scalar(query)
        if isinstance(user, UserModel):
            user.is_admin = False
            await self.session.commit()

    async def add_new_user(self, event: TelegramObject):
        stmt = select(UserModel).where(UserModel.id == event.from_user.id)
        user = await self.session.scalar(stmt)
        if user is None:
            user = UserModel(
                id=event.from_user.id,
                name=event.from_user.username,
                is_admin=(event.from_user.id == int(os.getenv('SUPER_ADMIN_ID'))),
                is_super_admin=(event.from_user.id == int(os.getenv('SUPER_ADMIN_ID'))),
                is_registered=False,
            )
            self.session.add(user)

        if user.name != event.from_user.username:
            #Дополнительная проверка на смену ника у пользователя
            user.name = event.from_user.username
        await self.session.commit()

    async def super_admin_check(self, event: TelegramObject):
        stmt = select(UserModel).where(UserModel.is_super_admin == 1)
        users = await self.session.scalars(stmt)
        for user in users:
            if user.id == event.from_user.id:
                return True
        return False

    async def admin_check(self, event: TelegramObject):
        stmt = select(UserModel).where(UserModel.is_admin == 1)
        users = await self.session.scalars(stmt)
        for user in users:
            if user.id == event.from_user.id:
                return True
        return False




