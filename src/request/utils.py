import jwt as pyjwt

from Users import Auth

async def update_jwt(jwt):
    rt = (await pyjwt.decode(jwt, 'secret', algorithms=['HS256']))['refresh_token']
    jwt = (await Auth.refresh_token(rt))['token']
    return jwt

async def append_rt(jwt):
    jwt['refresh_token'] = (await pyjwt.decode(jwt['token'], "secret", algorithms=["HS256"]))['refresh_token']
    return jwt

async def second_req(jwt, url, session):
    jwt = await update_jwt(jwt)
    async with session.post(url, headers={'Authorization': f'Bearer {jwt}'}) as res:
        if res.status == 200:
            return await res.json()
        return res.status