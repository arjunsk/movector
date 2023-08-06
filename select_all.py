from sqlalchemy import create_engine, Integer, String, select, desc
from sqlalchemy.orm import declarative_base, mapped_column, Session

from movector.sqlalchemy import VectorF32

engine = create_engine("mysql+pymysql://root:111@127.0.0.1:6001/a")
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(50))
    factors = mapped_column(VectorF32(3))


# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

session = Session(engine)

# SELECT * WHERE age > 30 ORDER BY salary DESC
stmt = select(User).where(User.id > 0).order_by(desc(User.name))

# Execute the query and fetch all records
result = session.execute(stmt).fetchall()

# Print the results
for row in result:
    print(row)
