import asyncio
import time

import asyncpg
import numpy as np
from pgvector.asyncpg import register_vector

table_name = "speedtest"
vec_len = 1024
num_inserts = 1024 * 8
num_vector_per_insert = 5


async def create_table(connection):
    await register_vector(connection)


async def insert_items(connection, num_items):
    tr = connection.transaction()
    await tr.start()
    for _ in range(num_items):
        embedding = np.random.rand(vec_len).tolist()
        await connection.execute("INSERT INTO speedtest (one_k_vector) VALUES ($1)", embedding)
    await tr.commit()


async def run_benchmark():
    conn_params = {
        "host": "127.0.0.1",
        "port": 5432,
        "user": "postgres",
        "password": "111",
    }

    async with asyncpg.create_pool(**conn_params) as pool:
        async with pool.acquire() as connection:
            await create_table(connection)
            start = time.time()
            await insert_items(connection, num_inserts * num_vector_per_insert)
            duration = time.time() - start

    print(f"Result: vector dim={vec_len} vectors "
          f"inserted={num_inserts * num_vector_per_insert} "
          f"insert/second={num_inserts * num_vector_per_insert / duration:.2f}")


if __name__ == "__main__":
    asyncio.run(run_benchmark())
