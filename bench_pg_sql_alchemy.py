# pg database
# CREATE EXTENSION vector;
# pg table
# CREATE TABLE speedtest (id bigserial PRIMARY KEY, one_k_vector vector(1024));

import time
import numpy as np
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker, mapped_column, DeclarativeBase

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


def run():
    # pgvector psycopg2 issue on PyCharm https://stackoverflow.com/a/72288416/1609570
    engine = create_engine("postgresql+psycopg2://postgres:111@127.0.0.1:5432")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    for i in range(num_inserts * num_vector_per_insert):
        item = Item(one_k_vector=np.random.rand(vec_len))
        session.add(item)
    session.commit()


start = time.time()
run()
duration = time.time() - start
print(f"Result: vector dim={vec_len} vectors "
      f"inserted={num_inserts * num_vector_per_insert} "
      f"insert/second={num_inserts * num_vector_per_insert / duration}")
