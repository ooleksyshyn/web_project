from orm.column.columns import Column
from orm.exceptions.exceptions import *
from orm.model.query import DataBaseQuery

import re


class ModelMeta(type):
    __name_RE = re.compile("[a-zA-Z]+")

    def __new__(mcs, name, bases, attrs):
        object_instance = super().__new__(mcs, name, bases, attrs)
        model_name = object_instance.__name__

        if model_name != "Model":
            ModelMeta.__check_primary_key(object_instance, name)

            ModelMeta.__check_table_name(name)

            ModelMeta.__create_table(object_instance, name)

            ModelMeta.__set_column_names(object_instance)

        return object_instance

    @staticmethod
    def __set_column_names(object_instance):
        for column_name, column_object in object_instance.__dict__.items():
            if isinstance(column_object, Column):
                column_object.column_name = column_name

    @staticmethod
    def __check_primary_key(object_instance, name):
        primary_keys = [
            column_name for column_name, column_object in object_instance.__dict__.items()
            if isinstance(column_object, Column) and column_object.primary_key
        ]

        if not primary_keys:
            raise NoPrimaryKeysError(f"Database {name} has no primary keys")

    @staticmethod
    def __check_table_name(name):
        if not ModelMeta.__name_RE.match(name):
            raise InvalidTableNameError(f"Table name {name} is invalid")

    @staticmethod
    def __create_table(object_instance, name):
        columns_description = ",".join([
            column_name + " " + column_object.string()
            for column_name, column_object in object_instance.__dict__.items()
            if isinstance(column_object, Column)
        ])

        query = f"create table if not exists {name} ({columns_description});"

        object_instance._connection.cursor.execute(query)


class Model(metaclass=ModelMeta):
    _connection = None

    def __init__(self, **kwargs):
        if not self._connection:
            raise ConnectionError("No database connected")
        DataBaseQuery.insert(self._connection, self.__class__.__name__, **kwargs)

    @classmethod
    def delete(cls, expression=None):
        DataBaseQuery.delete(cls._connection, cls.__name__, expression=expression)

    @classmethod
    def insert(cls, **kwargs):
        DataBaseQuery.insert(cls._connection, cls.__name__, **kwargs)

    @classmethod
    def select(cls, *args, expression=None):
        return DataBaseQuery.select(cls._connection, cls.__name__, *args, expression=expression)
