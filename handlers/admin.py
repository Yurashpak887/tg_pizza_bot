from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from filters.chat_types import ChatTypes, IsAdmin
from kbds.reply import admin_kb

admin_router = Router()
admin_router.message.filter(ChatTypes(["private"]), IsAdmin())

@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer('Що хочете зробити?', reply_markup=admin_kb)

@admin_router.message(F.text == "Я тільки подивитись")
async def starring_at_product(message: types.Message):
    await message.answer("ОК, ось список товарів")


@admin_router.message(F.text == "Змінити товар")
async def change_product(message: types.Message):
    await message.answer("ОК, список товарів")


@admin_router.message(F.text == "Видалити товар")
async def delete_product(message: types.Message):
    await message.answer("Виберіть товар(и) для видалення")


#Код ниже для машины состояний (FSM)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name': 'Введіть назву заново',
        'AddProduct:description': 'Введіть опис заново',
        'AddProduct:price': 'Введіть ціну заново',
    }



@admin_router.message(StateFilter(None), F.text == "Добавити товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter('*'), Command("відміна"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "відміна")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == None:
        return

    await state.clear()
    await message.answer("Дії відмінені!", reply_markup=admin_kb)


@admin_router.message(StateFilter("*"), Command("назад"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state == AddProduct.name:
        await message.answer('Попереднього кроку немає! назАбо введіть назву товару, або введіть "відміна"')
        return
    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ви повернулись до попереднього кроку! {AddProduct.texts[previous.state]} " )
            return
        previous = step


@admin_router.message(StateFilter(AddProduct.name), F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введіть опис товару")
    await state.set_state(AddProduct.description)


@admin_router.message(StateFilter(AddProduct.description), F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите вартість товару")
    await state.set_state(AddProduct.price)


@admin_router.message(StateFilter(AddProduct.price), F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Надішліть зображення товару")
    await state.set_state(AddProduct.image)


@admin_router.message(StateFilter(AddProduct.image), F.photo)
async def add_image(message: types.Message, state: FSMContext):
    await state.update_data(photo = message.photo[-1].file_id)
    await message.answer("Товар добавлений", reply_markup=admin_kb)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()