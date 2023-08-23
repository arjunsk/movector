# CREATE TABLE speedtest (id int PRIMARY KEY, one_k_vector vecf32(1024));

import time

import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from movector.utils import to_db_binary

table_name = "speedtest"
vec_len = 1024
num_inserts = 1024 * 8
num_vector_per_insert = 1024


def run():
    engine = create_engine("mysql+pymysql://root:111@127.0.0.1:6001/a")
    Session = sessionmaker(bind=engine)
    session = Session()

    # pgvector manjaro run1: Result: vector dim=1024 vectors inserted=40960 insert/second=940.058913141791
    # pgvector macos   run1: Result: vector dim=1024 vectors inserted=40960 insert/second=509.90686489099716
    # mo       macos   run1: Result: vector dim=1024 vectors inserted=40960 insert/second=340.54838430904914 Split (v1)
    sql_insert = text("insert into speedtest (id, one_k_vector) "
                      "values(:index, (cast( cast(:data as BLOB) as vecf32(:vec_len))));")
    for i in range(num_inserts * num_vector_per_insert):
        arr = np.random.rand(vec_len)
        session.execute(sql_insert, {"index": i, "data": to_db_binary(arr), "vec_len": vec_len})
    session.commit()


start = time.time()
run()
duration = time.time() - start
print(f"Result: vector dim={vec_len} vectors "
      f"inserted={num_inserts * num_vector_per_insert} "
      f"insert/second={num_inserts * num_vector_per_insert / duration}")
