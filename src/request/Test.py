import asyncio

from aiogram.client.session import aiohttp

from request.Users import Auth, Meetings
import jwt as pyjwt
from pprint import pprint


async def main():
    async with aiohttp.ClientSession() as session:
        t = (await Auth.login('Hantaton06', '5QsyJbimuDwlB)DK'))['token']
        pprint(await Meetings.meetings(t, '2024-10-14T00:23:10.028081', '2024-12-14T20:23:10.028122'))

asyncio.run(main())