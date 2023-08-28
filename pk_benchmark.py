# CREATE DATABASE a;
# USE a;
# CREATE TABLE speedtest (id int PRIMARY KEY); -- inserted=40960 insert/second=55.50412412642426
# CREATE TABLE speedtest (id int); -- inserted=40960 insert/second=9041.47774448042

import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

table_name = "speedtest"
num_inserts = 1024 * 8
num_vector_per_insert = 5


def run():
    # engine = create_engine("mysql+pymysql://root:111@127.0.0.1:6001/a")
    engine = create_engine("postgresql+psycopg2://postgres:111@127.0.0.1:5432/a")
    Session = sessionmaker(bind=engine)
    session = Session()

    sql_insert = text("insert into speedtest (id) values(:id);")
    for i in range(num_inserts * num_vector_per_insert):
        session.execute(sql_insert, {"id": i})
    session.commit()


start = time.time()
run()
duration = time.time() - start
print(f"Result:"
      f"inserted={num_inserts * num_vector_per_insert} "
      f"insert/second={num_inserts * num_vector_per_insert / duration}")