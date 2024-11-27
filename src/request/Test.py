import asyncio

from aiogram.client.session import aiohttp

from request.Users import Auth, Meetings
import jwt as pyjwt


async def main():
    async with aiohttp.ClientSession() as session:
        t = (await Auth.login('Hantaton06', '5QsyJbimuDwlB)DK'))['token']
        async with session.get('https://test.vcc.uriit.ru/api/users?page=1&rowsPerPage=100&showDeleted=false') as res:
            # data = (await res.json())['data']
            print(res.status)
        for i in data:
            ididi = i['id']
            async with session.delete(f'https://test.vcc.uriit.ru/api/users/{ididi}', headers={'Authorization': f'Bearer {t}'}) as res:
                print(res.status)

asyncio.run(main())