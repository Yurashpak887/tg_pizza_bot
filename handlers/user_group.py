from string import punctuation

from aiogram import F, Bot, types, Router
from aiogram.filters import Command
from filters.chat_types import ChatTypes

user_group_router = Router()
user_group_router.message.filter(ChatTypes(['group', 'supergroup']))



@user_group_router.message(Command('admin'))
async def get_admins(message: types.Message, bot:Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)
    print(admins_list)

    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == 'administrator' or member.status == "creator" or member.status == "owner"
    ]
    bot.my_admins_list = admins_list
    print(bot.my_admins_list)
    if message.from_user.id in admins_list:
        await message.delete()

restricted_word = {'кабан', 'хомяк', 'test'}

def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))

@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_word.intersection(message.text.lower().split()):
        await message.answer(f"{message.from_user.username}, зберігайте порядок в чаті! ")
        await message.delete()