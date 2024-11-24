import aiohttp
import asyncio


class Auth:
    @staticmethod
    async def register(login, password, email, lastname, firstname, middlename, phone, birthday, releid, typeusr) -> status:
        async with aiohttp.ClientSession() as session:
            async with session.post('https://test.vcc.uriit.ru/auth/register', json={
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
    async def login(login, passwd):
        async with aiohttp.ClientSession() as session:
            async with session.post('https://test.vcc.uriit.ru/auth/login', json={
                "login": login,
                "password": passwd,
                "fingerprint": {}
            }) as res:
                if res.status == 200:
                    return res.json()
                return res.status
