import asyncio

from aiogram.client.session import aiohttp

from request.Users import Auth, Meetings
import jwt as pyjwt
from pprint import pprint


async def main():
    t = (await Auth.login('hantaton10', '14Jiuqnr1sWWvo6G'))
    # pprint(await Meetings.meetings(t['token'], '2024-10-14T00:23:10.028081', '2024-12-14T20:23:10.028122', userId=t['user']['id']))
    print(t['token'])

asyncio.run(main())