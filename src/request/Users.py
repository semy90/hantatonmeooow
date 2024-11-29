import base64

import aiohttp
import asyncio

from request.utils import append_rt, second_req, jwttort


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
                    return await append_rt(await res.json())
                return res.status

    @staticmethod
    async def logout(jwt):
        """Log out| return string
        "string"
        """
        async with aiohttp.ClientSession() as session:
            url = 'https://test.vcc.uriit.ru/api/auth/logout'
            async with session.post(url, headers={'Authorization': f'Bearer {jwt}'}) as res:
                if res.status == 200:
                    return await res.json()
                if res.status == 401:
                    return await second_req(jwt, url, session, {})
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
                    return await append_rt(await res.json())
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
                    return await append_rt(await res.json())
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
        url = f'https://test.vcc.uriit.ru/api/role?page={page}&rowsPerPage={rowpage}&sort_by={sort}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"Authorization": f"Bearer {jwt}"}) as res:
                if res.status == 200:
                    return await res.json()
                if res.status == 401:
                    return await second_req(jwt, url, session, {})
                return res.status

    @staticmethod
    async def permissions(jwt, ends="ends"):
        """Возвращает все разрешения
        ["string"]"""
        url = f'https://test.vcc.uriit.ru/api/role/permissions?ends={ends}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={"Authorization": f'Bearer {jwt}'}) as res:
                if res.status == 200:
                    return await res.json()
                if res.status == 401:
                    return await second_req(jwt, url, session, {})
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
        url = f'https://test.vcc.uriit.ru/api/role/{role_id}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={'Authorization': f'Bearer {jwt}'}) as res:
                if res.status == 200:
                    return await res.json()
                if res.status == 401:
                    return await second_req(jwt, url, session, {})
                return res.status

    @staticmethod
    async def role_permission(jwt, role_id, permission):
        """{
            "name": "string",
            "description": "string",
            "id": 0,
            "permissions": [
            "string"
            ]
        }"""
        url = f'https://test.vcc.uriit.ru/api/role/{role_id}/permissions'
        async with aiohttp.ClientSession() as session:
            json = {[
                permission
            ]}
            async with session.put(url, headers={'Authorization': f'Bearer {jwt}'},
                                   json=json) as res:
                if res.status == 200:
                    return await res.json()
                if res.status == 401:
                    return await second_req(jwt, url, session, json)
                return res.status


class Account:
    @staticmethod
    async def info(jwt):
        url = f'https://test.vcc.uriit.ru/api/account/user-info'
        async with aiohttp.ClientSession() as session:
            json = {}
            async with session.get(url, headers={'Authorization': f'Bearer {jwt}'}) as res:
                if res.status == 200:
                    return await res.json()
                if res.status == 401:
                    return await second_req(jwt, url, session, json)
                return res.status

    @staticmethod
    async def refact_info(jwt, first_name=None, last_name=None, middle_name=None, email=None, phone=None,
                          birthday=None):
        url = f'https://test.vcc.uriit.ru/api/account/user-info'
        async with aiohttp.ClientSession() as session:
            import json
            data_us = jwt.split('.')[1]
            data_us = data_us.encode('utf-8')
            data_us = base64.b64decode(data_us + b'=' * (-len(data_us) % 4))
            data_us = data_us.decode('utf-8')
            data_us = json.loads(data_us)

            first_name = first_name or data_us['first_name']
            last_name = last_name or data_us['last_name']
            middle_name = middle_name or data_us['middle_name']
            email = email or data_us['email']
            phone = phone or data_us['phone']
            birthday = birthday or data_us['birthday']
            json = {
                "firstName": first_name,
                "lastName": last_name,
                "middleName": middle_name,
                "email": email,
                "phone": phone,
                "birthday": birthday
            }
            async with session.post(url, headers={'Authorization': f'Bearer {jwt}'}, json=json) as res:
                if res.status == 200:
                    return await res.json()
                if res.status == 401:
                    return await second_req(jwt, url, session, json)
                return res.status


class Meetings:
    @staticmethod
    async def meetings(jwt, fromDatetime, toDatetime, userId=None, buildingId=None, roomId=None, page=1, sort_by='id',
                       rowsPerPage=101,
                       state='booked'):
        url = f'https://test.vcc.uriit.ru/api/meetings'
        params = {
            'fromDatetime': fromDatetime,
            'toDatetime': toDatetime,
            'page': page,
            'userId': userId,
            'sort_by': sort_by,
            'rowsPerPage': rowsPerPage,
            'state': state
        }
        if not buildingId is None:
            params['buildingId'] = buildingId
        if not roomId is None:
            params['roomId'] = roomId
        while True:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, headers={'Authorization': f'Bearer {jwt}'}) as res:
                    if res.status == 200:
                        return (await res.json())['data']
                    if res.status == 401:
                        return (await second_req(jwt, url, session, {}))['data']
                    if res.status not in [200, 401]:
                        return res.status

    @staticmethod
    async def create_meetings(jwt, name: str, isMicrophoneOn: bool, isVideoOn: bool, isWaitingRoomEnabled: bool,
                              participantsCount: int, startedAt: str,
                              durationx: int, sendNotificationsAt: str, isGovernorPresents=False,
                              isNotifyAccepted=False, backend='cisco', state="booked", isVirtual=False, force=True):
        url = f'https://test.vcc.uriit.ru/api/meetings'
        id_org = (await jwttort(jwt))['user']
        params = {
            'force': 'true' if force else 'false'
        }
        json = {
            "name": name,
            "ciscoSettings": {
                "isMicrophoneOn": 'true' if isMicrophoneOn else 'false',
                "isVideoOn": 'true' if isVideoOn else 'false',
                "isWaitingRoomEnabled": 'true' if isWaitingRoomEnabled else 'false',
                "needVideoRecording": 'false'
            },
            "participantsCount": participantsCount,
            "startedAt": startedAt,
            "duration": durationx,
            'isVirtual': 'true' if isVirtual else 'false',
            "participants": [
                {
                    'id': id_org["id"]
                },
                {
                    "email": id_org.get('email'),
                    "lastName": id_org.get('lastName'),
                    "firstName": id_org.get('firstName'),
                    "middleName": id_org.get('middleName')
                }
            ],
            "sendNotificationsAt": sendNotificationsAt,
            "recurrenceUpdateType": "only",
            'isGovernorPresents': 'true' if isGovernorPresents else 'false',
            'isNotifyAccepted': 'true' if isNotifyAccepted else 'false',
            "organizedBy": {"id": id_org["id"]},
            'backend': backend,
            "state": state
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json, headers={'Authorization': f'Bearer {jwt}'}, params=params) as res:
                if res.status == 201:
                    return await res.json()
                if res.status == 401:
                    return await second_req(jwt, url, session, json)
                if res.status == 422:
                    return await res.json()
                return res.status

    @staticmethod
    async def current_meetings(jwt, meetingId):
        url = f'https://test.vcc.uriit.ru/api/meetings/{meetingId}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                if res.status == 200:
                    return await res.json()
                if res.status == 401:
                    return await second_req(jwt, url, session, {})
                return res.status


class Departments:
    @staticmethod
    async def current_department(jwt, departmentId):
        url = f'https://test.vcc.uriit.ru/api/departments/{departmentId}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                if res.status == 200:
                    return await res.json()
                if res.status == 401:
                    return await second_req(jwt, url, session, {})
                return res.status
