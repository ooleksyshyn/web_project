class Expression:
    def __init__(self, first_operand, operator, second_operand):
        self._string = f"({first_operand}{operator}{second_operand})"

    def __str__(self):
        return self._string

    def __or__(self, other):
        return f"{str(self)} or {str(other)}"

    def __and__(self, other):
        return f"{str(self)} and {str(other)}"

    def not_(self):
        return f"(not {str(self)})"


class DataBaseQuery:
    @staticmethod
    def insert(database_connection, table_name, **kwargs):
        columns = ", ".join(list(kwargs.keys()))

        values = ", ".join([
            f"'{value}'" if isinstance(value, str) else str(value) for value in kwargs.values()
        ])

        query = f"insert into {table_name} ({columns}) values ({values})"
        database_connection.execute(query)

    @staticmethod
    def delete(database_connection, table_name, expression=None):
        if expression:
            where_option = f"where {str(expression)}"

        query = f"delete from {table_name} {where_option};"
        database_connection.execute(query)

    @staticmethod
    def select(database_connection, table_name=None, *args, expression=None):
        fields = ", ".join(list(args)) if args else "*"

        where_option = f"where {str(expression)}" if expression else ""

        query = f"select {fields} from {table_name} {where_option};"

        return database_connection.execute(query)
