import asyncio
import time

import numpy as np

from movector.utils import to_db, to_db_binary

vec_len = 1024
num_inserts = 1024 * 8
num_vector_per_insert = 5


async def run_text(num_items):
    for _ in range(num_items):
        embedding = np.random.rand(vec_len)
        a = to_db(embedding)


async def run_bin(num_items):
    for _ in range(num_items):
        embedding = np.random.rand(vec_len)
        a = to_db_binary(embedding)


async def run_benchmark():
    start = time.time()
    await run_text(num_inserts * num_vector_per_insert)
    duration = time.time() - start

    print(f"Result: vector dim={vec_len} vectors "
          f"inserted={num_inserts * num_vector_per_insert} "
          f"insert/second={num_inserts * num_vector_per_insert / duration:.2f}")

    start2 = time.time()
    await run_bin(num_inserts * num_vector_per_insert)
    duration = time.time() - start2

    print(f"Result: vector dim={vec_len} vectors "
          f"inserted={num_inserts * num_vector_per_insert} "
          f"insert/second={num_inserts * num_vector_per_insert / duration:.2f}")


if __name__ == "__main__":
    asyncio.run(run_benchmark())
