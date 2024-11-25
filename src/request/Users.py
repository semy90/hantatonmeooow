import aiohttp
import asyncio

from typing_extensions import runtime


class Auth:
    @staticmethod
    async def register(login, password, email, lastname, firstname, middlename, phone, birthday, releid, typeusr):
        """return STATUS"""
        async with aiohttp.ClientSession() as session:
            async with session.post('https://test.vcc.uriit.ru/api/auth/register', json={
                "login": login,
                "password": password,
                "email": email,
                "lastName": lastname,
                "firstName": firstname,
                "middleName": middlename,
                "phone": phone,
                "birthday": birthday,
                "roleId": releid,
                "type": typeusr
            }) as res:
                return res.status

    @staticmethod
    def login(login, passwd):
        """return DICT_INFO_USER or STATUS"""
        with aiohttp.ClientSession() as session:
            with session.post('https://test.vcc.uriit.ru/api/auth/login', json={
                "login": login,
                "password": passwd,
                "fingerprint": {}
            }) as res:
                if res.status == 200:
                    return res.json()
                return res.status

    @staticmethod
    async def refresh_token(token):
        """update User -> DictUser"""
        with aiohttp.ClientSession() as session:
            with session.post('https://test.vcc.uriit.ru/api/auth/refresh', json={
                "token": token
            }) as res:
                if res.status == 200:
                    return res.json()
                return res.status

    @staticmethod
    async def reset_password(email: str):
        """return STATUS"""
        with aiohttp.ClientSession() as session:
            with session.post('https://test.vcc.uriit.ru/api/auth/reset-password', json={
                "email": email
            }) as res:
                if res.status == 200:
                    return res.status
                return res.status

    @staticmethod
    async def reset_password_confirm(newpasswd: str, resettoken: str):
        """return STATUS"""
        with aiohttp.ClientSession() as session:
            with session.post('https://test.vcc.uriit.ru/api/auth/reset-password-confirm', json={
                "newPassword": newpasswd,
                "resetToken": resettoken
            }) as res:
                if res.status == 200:
                    return res.status
                return res.status

    @staticmethod
    async def ldap_login(login: str, password: str):
        """Вернёт код ошибки или Юзера"""
        async with aiohttp.ClientSession() as session:
            with session.post('https://test.vcc.uriit.ru/api/auth/ldap/login', json={
                "login": login,
                "password": password,
                "fingerprint": {}
            }) as res:
                if res.status == 200:
                    return res.json
                return res.status

