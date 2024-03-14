from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_add_product, orm_update_product, orm_delete_product, orm_get_product, orm_get_products
from filters.chat_types import ChatTypes, IsAdmin
from kbds.inline import get_callback_btns
from kbds.reply import admin_kb

admin_router = Router()
admin_router.message.filter(ChatTypes(["private"]), IsAdmin())


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

@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer('Що хочете зробити?', reply_markup=admin_kb)


@admin_router.message(F.text == "Асортимент")
async def starring_at_product(message: types.Message, session:AsyncSession):
    result = await orm_get_products(session)
    for product in result:
        if product:
            await message.answer_photo(
                product.image,
                caption=f'<strong>{product.name}</strong>\n{product.description}\n{round(product.price, 2)}',
                reply_markup=get_callback_btns(btns={
                    "Видалити": f'delete_ {product.id}'
                })

            )
    await message.answer("ОК, ось список товарів")


@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product(callback: types.CallbackQuery, session:AsyncSession):
    product_id = callback.data.split('_')[-1]
    await orm_delete_product(session, int(product_id))
    await callback.message.answer("Товар видалено!")







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
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image = message.photo[-1].file_id)

    await message.answer("Товар добавлений", reply_markup=admin_kb)
    #add data to db
    try:
        data = await state.get_data()
        await orm_add_product(session, data)
        await state.clear()
    except Exception as s:
        await message.answer(f'Сталась помилка {s}. Зверніться до програміста', reply_markup=admin_kb)
        await state.clear()