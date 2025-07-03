from peewee import Model, SqliteDatabase, CharField, FloatField, DateTimeField, IntegrityError
import logging
from datetime import datetime
from config import DB_NAME

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Подключение к базе данных
DATABASE = SqliteDatabase(DB_NAME)

# Базовый класс для модоелей
class BaseModel(Model):
    class Meta:
        database = DATABASE

# Модель пользователя
class User(BaseModel):
    user_id = CharField(unique=True)
    username = CharField(null=True)

# Модель для истории запросов
class QueryHistory(Model):
    user = CharField(index=True)
    query_type = CharField() # к примеру: 'crypto', 'fiat'
    currency = CharField() # какая валюта
    rate = FloatField() # курс валюты на момент запроса
    timestamp = DateTimeField(default=datetime.now, index=True)

    class Meta:
        database = DATABASE

# Функция для создания таблицы
def initialize_db():
    try:
        DATABASE.connect()
        DATABASE.create_tables([User, QueryHistory], safe=True)
        logger.info("База данных успешно инициализирована.")
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
    finally:
        if not DATABASE.is_closed():
            DATABASE.close()

# Функция для добавления нового пользователя
def add_user(user_id, username):
    try:
        user, created = User.get_or_create(user_id=user_id, defaults={'username' : username})
        if created:
            logger.info(f"Пользователь {user_id} успешно добавлен.")
        else:
            logger.info(f"Пользователь {user_id} уже существует.")
        return user, created
    except IntegrityError as e:
        logger.error(f"Ошибка при добавлении пользователя {user_id}: {e}")
    return None, False

# Функция для записи истории запрпосов
def add_query_history(user_id, query_type, currency, rate):
    try:
        QueryHistory.create(user=user_id, query_type=query_type, currency=currency, rate=rate)
        logger.info(f"Запись истории добавлена для пользователя {user_id}.")
    except Exception as e:
        logger.error(f"Ошибка при добавлении записи истории для пользователя {user_id}: {e}")

# Функция для получения истории запросов пользователя
def get_user_history(user_id, limit=10):
    try:
        return (QueryHistory.select().where(QueryHistory.user == user_id).order_by
                (QueryHistory.timestamp.desc()).limit(limit))
    except Exception as e:
        logger.error(f"Ошибка при получении истории запросов для пользователя {user_id}: {e}")
        return []

# Функция для удаления пользователя
def delete_user(user_id):
    try:
        user = User.get(User.user_id == user_id)
        user.delete_instance()
        logger.info(f"Пользователь {user_id} успешно удалён")
    except User.DoesNotExist:
        logger.warning(f"Пользователь {user_id} не найден.")
    except Exception as e:
        logger.error(f"Ошибка при удалении пользователя {user_id}: {e}")

# Функция для удаления истории запросов пользователя
def delete_user_history(user_id):
    try:
        QueryHistory.delete().where(QueryHistory.user == user_id).execute()
        logger.info(f"История запросов пользователя {user_id} успешно удалена.")
    except Exception as e:
        logger.error(f"Ошибка при удалении истории запросов пользователя {user_id}: {e}")