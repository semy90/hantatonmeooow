import jwt as pyjwt
import aiohttp
import base64
import json

async def jwttort(jwt):

    rt = (jwt['token'] if type(jwt) == dict else jwt).split('.')[1]
    rt = rt.encode('utf-8')
    rt = base64.b64decode(rt + b'=' * (-len(rt) % 4))
    rt = rt.decode('utf-8')
    rt = json.loads(rt)
    return rt

async def update_jwt(jwt, session):
    rt = (await pyjwt.decode(jwt, 'secret', algorithms=['HS256']))['refresh_token']
    async with session.post('https://test.vcc.uriit.ru/api/auth/refresh-token', json={
        "token": rt
    }) as res:
        if res.status == 200:
            jwt = await append_rt(await res.json())
    return jwt

async def append_rt(jwt):
    rt = await jwttort(jwt)
    jwt['refresh_token'] = rt['refresh_token']
    return jwt

async def second_req(jwt, url, session, json):
    jwt = await update_jwt(jwt, session)
    async with session.post(url, headers={'Authorization': f'Bearer {jwt}'}, json=json) as res:
        if res.status == 200:
            return await res.json()
        return res.status