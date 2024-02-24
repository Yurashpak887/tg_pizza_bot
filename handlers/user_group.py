from string import punctuation

from aiogram import F, types, Router
from filters.chat_types import ChatTypes
user_group_router = Router()
user_group_router.message.filter(ChatTypes(['group', 'supergroup']))


restricted_word = {'кабан', 'хомяк', 'test'}

def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))


@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_word.intersection(message.text.lower().split()):
        await message.answer(f"{message.from_user.username}, зберігайте порядок в чаті! ")
        await message.delete()