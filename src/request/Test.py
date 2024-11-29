import asyncio

from aiogram.client.session import aiohttp

from request.Users import Auth, Meetings
import jwt as pyjwt
from pprint import pprint


async def main():
    t = (await Auth.login('hantaton10', '14Jiuqnr1sWWvo6G'))
    token = t['token'].encode("utf-8")
    pprint(await Meetings.create_meetings(t,'ТЕСТМЯУ',1, 1,1, 11,"2024-11-29T00:00:00", 150, "2024-11-29T00:00:00","booked"))

asyncio.run(main())