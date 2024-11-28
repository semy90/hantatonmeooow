from aiogram import Router
from aiogram.types import Message


idk_router = Router(name=__name__)

@idk_router.message()
async def i_dont_understand(message: Message):
    await message.reply("Я вас не понимаю!😯")