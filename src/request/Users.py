import aiohttp
import asyncio

from sqlalchemy.sql.operators import endswith_op


class Auth:
    @staticmethod
    async def register(login, password, email, lastname, firstname, middlename, phone, birthday, roleid=5,
                       typeusr="native"):
        """return STATUS ||
        {
          "id": 0,
          "login": "string",
          "lastName": "string",
          "firstName": "string",
          "middleName": "string",
          "departmentId": 0,
          "post": "string",
          "email": "user@example.com",
          "priority": 3,
          "roleIds": [
            0
          ],
          "isActive": true,
          "phone": "string",
          "birthday": "2024-11-26",
          "createdAt": "2024-11-26T11:46:06.215Z",
          "deletedAt": "2024-11-26T11:46:06.215Z"
        }"""
        async with aiohttp.ClientSession() as session:
            async with session.post('https://test.vcc.uriit.ru/api/auth/register', json={
                "login": login,
                "password": password,
                "email": email,
                "lastName": lastname,
                "firstName": firstname,
                "middleName": middlename,
                "phone": phone,
                "birthday": birthday,
                "roleId": roleid,
                "type": typeusr
            }) as res:
                if res.status == 200:
                    return await res.json()
                return res.status

    @staticmethod
    async def login(login, passwd):
        """return DICT_INFO_USER or STATUS
        {
            "token": "string",
            "user": {
            "id": 0,
            "departmentId": 0,
            "post": "string",
            "permissions": [
              "string"
            ],
            "login": "string",
            "email": "user@example.com",
            "lastName": "string",
            "firstName": "string",
            "middleName": "string",
            "birthday": "2024-11-26",
            "phone": "string",
            "updatedAt": "2024-11-26T11:48:02.471Z",
            "priority": 0,
            "roles": [
              {
                "name": "string",
                "description": "string",
                "id": 0,
                "permissions": [
                  "string"
                ]
              }
            ],
            "department": {
              "name": "Очень важный департамент",
              "shortName": "string",
              "address": "string",
              "email": "user@example.com",
              "parentId": 0,
              "id": 0,
              "ldapName": "string"
            }
            },
            "tutorials_progress": {
            "additionalProp1": "2024-11-26T11:48:02.471Z",
            "additionalProp2": "2024-11-26T11:48:02.471Z",
            "additionalProp3": "2024-11-26T11:48:02.471Z"
            }
        }"""
        async with aiohttp.ClientSession() as session:
            async with session.post('https://test.vcc.uriit.ru/api/auth/login', json={
                "login": login,
                "password": passwd,
                "fingerprint": {}
            }) as res:
                if res.status == 200:
                    return await res.json()
                return res.status

    @staticmethod
    async def logout():
        """Log out| return string
        "string"
        """
        async with aiohttp.ClientSession() as session:
            async with session.post('https://test.vcc.uriit.ru/api/auth/logout',
                                    headers={'Authorization': f'Bearer {jwt}'}) as res:
                if res.status == 200:
                    return await res.json()
                return res.status

    @staticmethod
    async def refresh_token(ref_tok):
        """Обновляем JWT с помощью REF токена
        {
            "token": "string",
            "user": {
            "id": 0,
            "departmentId": 0,
            "post": "string",
            "permissions": [
              "string"
            ],
            "login": "string",
            "email": "user@example.com",
            "lastName": "string",
            "firstName": "string",
            "middleName": "string",
            "birthday": "2024-11-26",
            "phone": "string",
            "updatedAt": "2024-11-26T11:49:50.638Z",
            "priority": 0,
            "roles": [
              {
                "name": "string",
                "description": "string",
                "id": 0,
                "permissions": [
                  "string"
                ]
              }
            ],
            "department": {
              "name": "Очень важный департамент",
              "shortName": "string",
              "address": "string",
              "email": "user@example.com",
              "parentId": 0,
              "id": 0,
              "ldapName": "string"
            }
            },
            "tutorials_progress": {
            "additionalProp1": "2024-11-26T11:49:50.638Z",
            "additionalProp2": "2024-11-26T11:49:50.638Z",
            "additionalProp3": "2024-11-26T11:49:50.638Z"
            }
        }"""
        async with aiohttp.ClientSession() as session:
            async with session.post('https://test.vcc.uriit.ru/api/auth/refresh-token', json={
                "token": ref_tok
            }) as res:
                if res.status == 200:
                    return await res.json()
                return res.status

    @staticmethod
    async def reset_password(email):
        """Отправляет письмо на почту
        {
            "status": "ok",
            "warning": "string",
            "warning_info": [
            {}
            ]
        }"""
        async with aiohttp.ClientSession() as session:
            async with session.post('https://test.vcc.uriit.ru/api/auth/reset-password', json={
                "email": email
            }) as res:
                return res.status

    @staticmethod
    async def reset_password_confirm(newpasswd, token):
        """Подтверждение сброса
        {
            "status": "ok",
            "warning": "string",
            "warning_info": [
            {}
            ]
        }"""
        async with aiohttp.ClientSession() as session:
            async with session.post('https://test.vcc.uriit.ru/api/auth/reset-password-confirm', json={
                "newPassword": newpasswd,
                "resetToken": token
            }) as res:
                return res.status

    @staticmethod
    async def ldap_login(login, passwd):
        """Вход с помощью лдап
        {
            "token": "string",
            "user": {
            "id": 0,
            "departmentId": 0,
            "post": "string",
            "permissions": [
              "string"
            ],
            "login": "string",
            "email": "user@example.com",
            "lastName": "string",
            "firstName": "string",
            "middleName": "string",
            "birthday": "2024-11-26",
            "phone": "string",
            "updatedAt": "2024-11-26T11:58:56.446Z",
            "priority": 0,
            "roles": [
              {
                "name": "string",
                "description": "string",
                "id": 0,
                "permissions": [
                  "string"
                ]
              }
            ],
            "department": {
              "name": "Очень важный департамент",
              "shortName": "string",
              "address": "string",
              "email": "user@example.com",
              "parentId": 0,
              "id": 0,
              "ldapName": "string"
            }
            },
            "tutorials_progress": {
            "additionalProp1": "2024-11-26T11:58:56.446Z",
            "additionalProp2": "2024-11-26T11:58:56.446Z",
            "additionalProp3": "2024-11-26T11:58:56.446Z"
            }
        }"""
        async with aiohttp.ClientSession() as session:
            async with session.post('https://test.vcc.uriit.ru/api/auth/ldap/login', json={
                "login": login,
                "password": passwd,
                "fingerprint": {}
            }) as res:
                if res.status == 200:
                    return await res.json()
                return res.status


class Role:
    @staticmethod
    async def role(jwt, page=1, rowpage=101, sort='id'):
        """Возвращает все роли
        {
            "rowsPerPage": 0,
            "page": 0,
            "rowsNumber": 0,
            "showDeleted": false,
            "data": [
            {
              "name": "string",
              "description": "string",
              "id": 0,
              "permissions": [
                "string"
              ]
            }
            ],
            "sortBy": "id"
        }"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://test.vcc.uriit.ru/role?page={page}&rowsPerPage={rowpage}&sort_by={sort}',
                    headers={"Authorization": f"Bearer {jwt}"}) as res:
                if res.status == 200:
                    return await res.json()
                return res.status

    @staticmethod
    async def permissions(jwt, ends="ends"):
        """Возвращает все разрешения
        ["string"]"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://test.vcc.uriit.ru/role/permissions?ends={ends}',
                                   headers={"Authorization": f'Bearer {jwt}'}) as res:
                if res.status == 200:
                    return await res.json()
                return res.status

    @staticmethod
    async def get_role(jwt, role_id):
        """Возвращает роль по id(1, ...)
        {
            "name": "string",
            "description": "string",
            "id": 0,
            "permissions": [
            "string"
            ]
        }"""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://test.vcc.uriit.ru/api/role/{role_id}',
                                   headers={'Authorization': f'Bearer {jwt}'}) as res:
                if res.status == 200:
                    return await res.json()
                return res.status

    @staticmethod
    async def role_permission(role_id, permission):
        """{
            "name": "string",
            "description": "string",
            "id": 0,
            "permissions": [
            "string"
            ]
        }"""
        async with aiohttp.ClientSession() as session:
            async with session.put(f'https://test.vcc.uriit.ru/api/role/{role_id}/permissions',
                                   headers={'Authorization': f'Bearer {jwt}'},
                                   json={[
                                       permission
                                   ]}) as res:
                if res.status == 200:
                    return await res.json()
                return res.status


async def mimi():
    t = (Auth.refresh_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImlkIjo1NDksImRlcGFydG1lbnRfaWQiOjIsInBvc3QiOm51bGwsInBlcm1pc3Npb25zIjpbInJvbGUubGlzdCIsImdyb3VwLmRlbGV0ZSIsImVtYWlsX3RlbXBsYXRlcy5saXN0IiwidXNlci5saXN0Iiwic2V0dGluZy5saXN0IiwibWVldGluZy51cGRhdGUiLCJtZWV0aW5nLmRlbGV0ZSIsImV2ZW50Lmxpc3QiLCJ1c2VyLmNyZWF0ZV9wdWJsaWMiLCJtZWV0aW5nLmNyZWF0ZSIsImdyb3VwLnVwZGF0ZSIsImRlcGFydG1lbnQubGlzdCIsImJ1aWxkaW5nLmxpc3QiLCJwZXJtYW5lbnRfcm9vbS5saXN0IiwiZ3JvdXAubGlzdCIsInN0YXRpc3RpY3MubGlzdCIsIm11bmljaXBhbF9hcmVhLmxpc3QiLCJtZWV0aW5nLmxpc3QiLCJyb29tLmxpc3QiLCJmaWxlLmxpc3QiLCJyb2xlLnBlcm1pc3Npb25zX2xpc3QiLCJ1c2VyLnVwZGF0ZV9wdWJsaWMiLCJmaWxlLmNyZWF0ZSIsImdyb3VwLmNyZWF0ZSJdLCJsb2dpbiI6IkhhbnRhdG9uMDYiLCJlbWFpbCI6ImhhbnRhdG9uMDYuaEBtYWlsLnJ1IiwibGFzdF9uYW1lIjoiXHUwNDI1XHUwNDMwXHUwNDNkXHUwNDQyXHUwNDMwXHUwNDQyXHUwNDNlXHUwNDNkXHUwNDNlXHUwNDMyIiwiZmlyc3RfbmFtZSI6Ilx1MDQyNVx1MDQzMFx1MDQzZFx1MDQ0Mlx1MDQzMFx1MDQ0Mlx1MDQzZVx1MDQzZCIsIm1pZGRsZV9uYW1lIjoiIiwiYmlydGhkYXkiOm51bGwsInBob25lIjpudWxsLCJ1cGRhdGVkX2F0IjoxNzMyMjg3OTY2LjAsInByaW9yaXR5IjoyLCJyb2xlcyI6W3sibmFtZSI6Ilx1MDQxZVx1MDQ0MFx1MDQzM1x1MDQzMFx1MDQzZFx1MDQzOFx1MDQzN1x1MDQzMFx1MDQ0Mlx1MDQzZVx1MDQ0MCIsImRlc2NyaXB0aW9uIjoiXHUwNDFlXHUwNDQwXHUwNDMzXHUwNDMwXHUwNDNkXHUwNDM4XHUwNDM3XHUwNDMwXHUwNDQyXHUwNDNlXHUwNDQwIFx1MDQzMlx1MDQzOFx1MDQzNFx1MDQzNVx1MDQzZVx1MDQzYVx1MDQzZVx1MDQzZFx1MDQ0NFx1MDQzNVx1MDQ0MFx1MDQzNVx1MDQzZFx1MDQ0Nlx1MDQzOFx1MDQzOSIsImlkIjozLCJwZXJtaXNzaW9ucyI6WyJidWlsZGluZy5saXN0IiwiZGVwYXJ0bWVudC5saXN0IiwiZW1haWxfdGVtcGxhdGVzLmxpc3QiLCJldmVudC5saXN0IiwiZmlsZS5saXN0IiwibWVldGluZy5jcmVhdGUiLCJtZWV0aW5nLmRlbGV0ZSIsIm1lZXRpbmcubGlzdCIsIm1lZXRpbmcudXBkYXRlIiwibXVuaWNpcGFsX2FyZWEubGlzdCIsInJvbGUubGlzdCIsInJvbGUucGVybWlzc2lvbnNfbGlzdCIsInJvb20ubGlzdCIsInNldHRpbmcubGlzdCIsInVzZXIubGlzdCIsInN0YXRpc3RpY3MubGlzdCIsImZpbGUuY3JlYXRlIiwicGVybWFuZW50X3Jvb20ubGlzdCIsImdyb3VwLmxpc3QiLCJncm91cC5jcmVhdGUiLCJncm91cC51cGRhdGUiLCJncm91cC5kZWxldGUiLCJwZXJtYW5lbnRfcm9vbS5saXN0IiwidXNlci5jcmVhdGVfcHVibGljIiwidXNlci51cGRhdGVfcHVibGljIl19XX0sInRva2VuX2V4cGlyZWRfYXQiOjE3MzI1NzMzODAuMCwidG9rZW5fY3JlYXRlZF9hdCI6MTczMjU1ODk4MC4wLCJyZWZyZXNoX3Rva2VuIjoiZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6STFOaUo5LmV5SjFjMlZ5WDJsa0lqbzFORGtzSW1WNGNDSTZNVGN6TXpFMk16YzRNQzR3TENKMWNHUWlPakUzTXpJeU9EYzVOall1TUN3aWRIbHdJam9pY21WbWNtVnphQ0o5LnhCbDVDUGtZc25IOW96M0hXZWkydHJMUjJQN0NOQzBmSUpMMF93Y05tUmsifQ.COBvD6aXjU9bURRNXow94rv9bhlIBVLSteNUn3Jyp-o'))
    print(t)

asyncio.run(mimi())