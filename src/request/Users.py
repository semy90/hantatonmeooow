import aiohttp
import asyncio


class Auth:
    @staticmethod
    async def register(login, password, email, lastname, firstname, middlename, phone, birthday, roleid=5,
                       typeusr="native"):
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
                "roleId": roleid,
                "type": typeusr
            }) as res:
                return res.status

    @staticmethod
    async def login(login, passwd):
        """return DICT_INFO_USER or STATUS"""
        async with aiohttp.ClientSession() as session:
            async with session.post('https://test.vcc.uriit.ru/api/auth/login', json={
                "login": login,
                "password": passwd,
                "fingerprint": {}
            }) as res:
                if res.status == 200:
                    return await res.json()
                return res.status
