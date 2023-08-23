# CREATE TABLE speedtest (id int PRIMARY KEY, one_k_vector vecf32(1024));

import time

import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from movector.utils import to_db_binary

table_name = "speedtest"
vec_len = 1024
num_inserts = 1024 * 8
num_vector_per_insert = 5


def run():
    engine = create_engine("mysql+pymysql://root:111@127.0.0.1:6001/a")
    Session = sessionmaker(bind=engine)
    session = Session()

    # mo macos vector dim=1024 vectors inserted=40960 insert/second=2700.82418588553   Binary Insert
    # mo macos vector dim=1024 vectors inserted=40960 insert/second=3395.4617004321026 Hex Insert
    sql_insert = text("insert into speedtest (id, one_k_vector) "
                      "values(:id, (cast( cast(:data as BLOB) as vecf32(:vec_len))));")
    for i in range(num_inserts * num_vector_per_insert):
        arr = np.random.rand(vec_len)
        # print(arr)
        session.execute(sql_insert, {"id": i, "data": to_db_binary(arr), "vec_len": vec_len})
    session.commit()


start = time.time()
run()
duration = time.time() - start
print(f"Result: vector dim={vec_len} vectors "
      f"inserted={num_inserts * num_vector_per_insert} "
      f"insert/second={num_inserts * num_vector_per_insert / duration}")
