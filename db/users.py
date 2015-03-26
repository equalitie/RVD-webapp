from db import users_table, fetch_one
from sqlalchemy.sql import select


def get_user_by_id(user_id):
    s = select([users_table]).where(users_table.c.id == user_id)
    item = fetch_one(s)
    return item