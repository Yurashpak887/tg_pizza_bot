import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from dotenv import load_dotenv, find_dotenv

from middlewares.db import DataBaseSession

load_dotenv(find_dotenv())
from database.engine import create_db, drop_db, session_maker

from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
from handlers.admin import admin_router
from common.bot_cmds_list import private


ALLOWED_UPDATES = ['message', 'edited_message', 'callback_query']

bot = Bot(token=os.getenv('TOKEN'))
bot.my_admins_list = []
dp = Dispatcher()



dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)




async def main():
    await create_db()
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())

    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
asyncio.run(main())