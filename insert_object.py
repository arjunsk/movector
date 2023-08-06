from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import declarative_base, mapped_column, Session

from movector.sqlalchemy import VectorF32

engine = create_engine("mysql+pymysql://root:111@127.0.0.1:6001/a")
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String(50))
    factors = mapped_column(VectorF32(3))


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session = Session(engine)

person1 = User(name='John Doe', factors=[1, 2, 3])
person2 = User(name='Jane Smith', factors=[4, 5, 6])

session.add(person1)
session.add(person2)

session.commit()

user = session.get(User, 1)
print('user-based recs:', [user.id, user.factors])

session.close()
