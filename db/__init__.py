from rvd import app
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
echo = True if app.config['SERVER_ENV'] == "DEV" else False

db_engine = 'mysql+mysqldb://{}:{}@{}/{}?charset=utf8'.format(
    app.config['DB_USER'], app.config['DB_PASS'], app.config['DB_HOST'], app.config['DB_NAME']
)
engine = create_engine(db_engine, echo=echo, logging_name="EQ")
metadata = MetaData(bind=engine)
eq_Session = sessionmaker(bind=engine, autocommit=True)
session = eq_Session()
users_table = Table('users', metadata, autoload=True, autoload_with=engine)


def fetch_one(query):
    result_proxy = session.execute(query)
    row_proxy = result_proxy.fetchone()
    if row_proxy is None:
        return None
    item = dict(zip(row_proxy.keys(), row_proxy.values()))
    return item