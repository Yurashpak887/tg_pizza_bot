from aiogram import Bot, types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from filters.chat_types import ChatTypes
user_private_router = Router()
user_private_router.message.filter(ChatTypes(['private']))

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Це була команда старт")


@user_private_router.message(or_f(Command('menu'), (F.text.lower().contains('меню'))))
async def menu(message: types.Message):
    await message.answer("Вот меню!")


@user_private_router.message(F.text.lower().contains('про нас'))
@user_private_router.message(Command("about"))
async def about(message: types.Message):
    await message.answer('Про нас')


@user_private_router.message(F.text.lower().contains('оплата'))
@user_private_router.message(Command("payment"))
async def payment(message: types.Message):
    await message.answer("Варіанти оплати")


@user_private_router.message((F.text.lower().contains('доставк')) | (F.text.lower()=='варіанти доставки'))
@user_private_router.message(Command("shipping"))
async def shipping(message: types.Message):
    await message.answer("Варіанти доставки")


@user_private_router.message(F.text.lower() =='варіанти доставки')
async def echo(message: types.Message, bot:Bot):
    await bot.send_message(message.from_user.id, message.text)
    await message.answer(str(message.from_user.id))
    await message.answer("Спрацював магічний метод")


