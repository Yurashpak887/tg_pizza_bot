from aiogram import Bot, types, Router, F
from aiogram.filters import CommandStart, Command, or_f
from filters.chat_types import ChatTypes

from kbds import reply

user_private_router = Router()
user_private_router.message.filter(ChatTypes(['private']))

@user_private_router.message(F.text.lower().contains('головн'))
@user_private_router.message(Command("home"))
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привіт! Я віртуальний помічник нашого закладу!", reply_markup=reply.start_kb2.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Що вас цікавить?'
    )
    )


@user_private_router.message(or_f(Command('menu'), (F.text.lower().contains('меню'))))
async def menu(message: types.Message):
    await message.answer("Вот меню!", reply_markup=reply.del_kdb)


@user_private_router.message(F.text.lower().contains('залишити відгук'))
@user_private_router.message(Command("response"))
async def about(message: types.Message):
    await message.answer('Відгук', reply_markup=reply.test_kb)


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


@user_private_router.message(F.location)
async def get_location(message: types.Message):
    await message.answer(f"Локація отримана")
    await message.answer(str(message.location))

@user_private_router.message(F.contact)
async def get_location(message: types.Message):
    await message.answer(f"Номер отриманий")
    await message.answer(str(message.contact.phone_number))