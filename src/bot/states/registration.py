from aiogram.fsm.state import StatesGroup, State

# "login": "string",
# "password": "string",
# "email": "user@example.com",
# "lastName": "string",
# "firstName": "string",
# "middleName": "string",
# "phone": "string",
# "birthday": "2024-11-25",
# "roleId": 5,
# "type": "native"
class RegistrationState(StatesGroup):
    waiting_login = State()
    waiting_email = State()
    waiting_password = State()
    waiting_lastname = State()
    waiting_firstname = State()
    waiting_middlename = State()
    waiting_phone = State()
    waiting_bithday = State()
    confirm_state = State()
