# pg database
# CREATE EXTENSION vector;
# pg table
# CREATE TABLE speedtest (id bigserial PRIMARY KEY, one_k_vector vector(1024));

import asyncio
import time

import numpy as np
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import mapped_column, DeclarativeBase

from movector.sqlalchemy import VectorF32

table_name = "speedtest"
vec_len = 1024
num_inserts = 1024 * 8
num_vector_per_insert = 5


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = table_name
    id = Column(Integer(), primary_key=True)
    one_k_vector = mapped_column(VectorF32(vec_len))


async def create_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def insert_items(session, num_items):
    items = [Item(one_k_vector=np.random.rand(vec_len).tolist()) for _ in range(num_items)]
    session.add_all(items)
    await session.commit()


async def run(engine):
    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as session:
        await insert_items(session, num_inserts * num_vector_per_insert)


async def async_main():
    engine = create_async_engine("mysql+asyncmy://root:111@127.0.0.1:6001/a", future=True)
    await create_database(engine)
    start = time.time()
    await run(engine)
    duration = time.time() - start
    print(f"Result: vector dim={vec_len} vectors "
          f"inserted={num_inserts * num_vector_per_insert} "
          f"insert/second={num_inserts * num_vector_per_insert / duration:.2f}")


if __name__ == "__main__":
    asyncio.run(async_main())

# Approach 1
# async def run():
#     # greenlet issue: https://appdividend.com/2022/03/19/how-to-solve-python-h-no-such-file-or-directory/
#     engine = create_async_engine("mysql+asyncmy://root:111@127.0.0.1:6001/a", future=True)
#     # engine = create_async_engine("mysql+aiosqlite://root:111@127.0.0.1:6001/a")
#
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
#     Session = async_sessionmaker(engine, expire_on_commit=False)
#
#     async with Session() as session:
#         for i in range(num_inserts * num_vector_per_insert):
#             item = Item(one_k_vector=np.random.rand(vec_len))
#             session.add(item)
#         await session.commit()
