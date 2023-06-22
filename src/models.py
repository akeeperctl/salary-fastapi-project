from sqlalchemy.orm import DeclarativeBase


# Определяем общий класс для всех моделей.
# Это необходимо для добавления моделей таблиц в metadata,
# а из metadata, посредством миграций, создадутся таблицы в БД
class Base(DeclarativeBase):
    pass
