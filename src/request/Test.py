import asyncio
import json

from aiogram.client.session import aiohttp

from request.Users import Auth, Meetings
import jwt as pyjwt
from pprint import pprint


async def main():
    t = (await Auth.login('hantaton10', '14Jiuqnr1sWWvo6G'))
    # pprint(await Meetings.meetings(t['token'], "2024-12-01T12:00:00",
    #                                '2024-11-08T12:00:00'))
    print(type(json.dumps(t)))


asyncio.run(main())
