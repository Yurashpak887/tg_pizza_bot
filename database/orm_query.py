from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product


async def orm_add_product(session: AsyncSession, data: dict):
    object = Product(name=data['name'], description=data['description'], price=float(data['price']), image=data['image'])
    session.add(object)
    await session.commit()




async def orm_get_products(session: AsyncSession):
    #Робимо селект з таблиці продукт
    query = select(Product)
    #В змінну резалт запихаєм в метод execute() - виконати.
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_product(session: AsyncSession, product_id: int):
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    return result.scalars()

async def orm_update_product(session: AsyncSession, product_id: int, data):
    query = update(Product).where(Product.id == product_id).values(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        image=data['image']
    )
    await session.execute(query)
    return await session.commit()

async def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    return await session.commit()