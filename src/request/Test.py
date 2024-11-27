import asyncio
from request.Users import Auth, Meetings
import jwt as pyjwt


async def main():
    t = (await Auth.login('Hantaton01', 't6vYHnNhBqN1F4(q'))['token']
    # print(await Meetings.meetings(t, '2024-11-14T00:23:10.028081', '2024-11-14T20:23:10.028122', 1, 1))
    print(await pyjwt.decode(t, 'secret', algorithms=['HS256']))

asyncio.run(main())