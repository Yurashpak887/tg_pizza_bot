import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.schema import MetaData

from database.models import Base

# Створюємо асинхронний об'єкт двигуна
engine = create_async_engine(os.getenv('DB_LITE'), echo=True)

# Створюємо сесію бази даних
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

metadata = MetaData()

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
