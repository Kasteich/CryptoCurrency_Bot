from peewee import Model, SqliteDatabase, CharField, FloatField, DateTimeField
import os
from datetime import datetime
from config import DB_NAME

# Подключение к базе данных
DATABASE = SqliteDatabase(DB_NAME)

# Модель пользователя
class User(Model):
    user_id = CharField(unique=True)
    username = CharField(null=True)

    class Meta:
        database = DATABASE

# Модель для истории запросов
class QueryHistory(Model):
    user = CharField()
    query_type = CharField() # к примеру: 'crypto', 'fiat'
    currency = CharField() # какая валюта
    rate = FloatField() # курс валюты на момент запроса
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        database = DATABASE

# Функция для создания таблицы
def initialize_db():
    DATABASE.connect()
    DATABASE.create_tables([User, QueryHistory], safe=True)
    DATABASE.close()

# Функция для добавления нового пользователя
def add_user(user_id, username):
    user, created = User.get_or_create(user_id=user_id, defaults={'username' : username})
    return user, created

# Функция для записи истории запрпосов
def add_query_history(user_id, query_type, currency, rate):
    QueryHistory.create(user=user_id, query_type=query_type, currency=currency, rate=rate)

# Функция для получения истории запросов пользователя
def get_user_history(user_id, limit=10):
    return (QueryHistory.select().where(QueryHistory.user == user_id).order_by
            (QueryHistory.timestamp.desc()).limit(limit))