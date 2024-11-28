def data_sender(data: dict) -> str:
    s = f'''💲Ваш профиль:
<b>Фамилия</b>: {data['lastName']}
<b>Имя</b>: {data['firstName']}
<b>Отчество</b>: {data['middleName']}
✉Почта: {data['email']}
📱Телефон: {data['phone']}
‼Ваша роль: {data['roles'][0]['name']}
Описание роли: {data['roles'][0]['description']}
🏛Департамент:
    😎Название: {data['department']['name']}({data['department']['shortName']})
    ❗Адрес: {data['department']['address']}
    ✉Почта: {data['department']['email']}
    '''
    return s


def data_for_change_name(data: dict) -> str:
    s = ""
    if data['lastname'] is not None:
        s += data['lastname'] + '\n'
    if data['firstname'] is not None:
        s += data['firstname'] + '\n'
    if data['middlename'] is not None:
        s += data['middlename']
    return s