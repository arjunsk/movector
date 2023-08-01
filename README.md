### MO Vector Python Client

Work in progress.

### Sample code:
```python
import implicit
from implicit.datasets.movielens import get_movielens

from sqlalchemy import create_engine, insert, select, text, Integer, String
from sqlalchemy.orm import declarative_base, mapped_column, Session

from movector.sqlalchemy import VectorF32

engine = create_engine("mysql+pymysql://root:111@127.0.0.1:6001/a")
with engine.connect() as conn:
    results = conn.execute(text("SELECT 42;"))

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = mapped_column(Integer, primary_key=True)
    factors = mapped_column(VectorF32(20))


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

titles, ratings = get_movielens('100k')
model = implicit.als.AlternatingLeastSquares(factors=20)
model.fit(ratings)

users = [dict(factors=factors) for i, factors in enumerate(model.user_factors)]

session = Session(engine)
session.execute(insert(User), users)

user = session.get(User, 70)
print('user-based recs:', [user.id, user.factors])

# Prints:
# user-based recs: [70, array([ 7.8333974 ,  8.490529  ,  8.774695  ,  9.268776  ,  6.0036736 ,
#         6.134292  ,  0.19642895,  7.596437  ,  2.9758034 ,  7.9472003 ,
#         4.068931  ,  0.58703905,  1.5298995 ,  5.9633737 ,  2.553488  ,
#         4.9483128 , 10.799758  ,  0.6393655 ,  7.034949  ,  6.145868  ],
#       dtype=float32)]
```

Async Support: https://github.com/sqlalchemy/sqlalchemy/blob/main/examples/asyncio/basic.py

Derived From: https://github.com/pgvector/pgvector-python/blob/master/pgvector/sqlalchemy/__init__.py

