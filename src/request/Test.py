import asyncio

from aiogram.client.session import aiohttp

from request.Users import Auth, Meetings
import jwt as pyjwt
from pprint import pprint


async def main():
    t = (await Auth.login('hantaton10', '14Jiuqnr1sWWvo6G'))
    pprint(await Meetings.create_meetings(t['token'], "ПРОШУПРОШУ ПРОШУУУ", True, True, True, 1, "2024-12-01T12:00:00", 120,
                                          '2024-11-08T12:00:00', state='booked'))
    # print(t['token'])


asyncio.run(main())
