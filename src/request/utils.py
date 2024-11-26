import jwt as pyjwt
import aiohttp

async def update_jwt(jwt, session):
    rt = (await pyjwt.decode(jwt, 'secret', algorithms=['HS256']))['refresh_token']
    async with session.post('https://test.vcc.uriit.ru/api/auth/refresh-token', json={
        "token": rt
    }) as res:
        if res.status == 200:
            jwt = await append_rt(await res.json())
    return jwt

async def append_rt(jwt):
    jwt['refresh_token'] = (await pyjwt.decode(jwt['token'], "secret", algorithms=["HS256"]))['refresh_token']
    return jwt

async def second_req(jwt, url, session):
    jwt = await update_jwt(jwt, session)
    async with session.post(url, headers={'Authorization': f'Bearer {jwt}'}) as res:
        if res.status == 200:
            return await res.json()
        return res.status