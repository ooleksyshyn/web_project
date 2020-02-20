import abc
from orm.model.query import Expression


class Column(metaclass=abc.ABCMeta):
    def __init__(self, primary_key=False, nullable=True):
        self._primary_key = primary_key
        self._nullable = nullable
        self.column_name = None
        self._type = None

    @property
    def primary_key(self):
        return self._primary_key

    def string(self):
        res = self._type
        if self.primary_key:
            res += " primary key"

        if self._nullable:
            res += " not null"

        return res

    def __eq__(self, other):
        return Expression(self.column_name, "=", f"'{other}'")

    def __ne__(self, other):
        return Expression(self.column_name, "!=", f"'{other}'")

    def __lt__(self, other):
        return Expression(self.column_name, "<", f"'{other}'")

    def __gt__(self, other):
        return Expression(self.column_name, ">", f"'{other}'")

    def __le__(self, other):
        return Expression(self.column_name, "<=", f"'{other}'")

    def __ge__(self, other):
        Expression(self.column_name, ">=", f"'{other}'")


class IntegerColumn(Column):
    def __init__(self, primary_key=False, nullable=True):
        super().__init__(primary_key, nullable)
        self._type = "integer"


class StringColumn(Column):
    def __init__(self, primary_key=False, nullable=True, max_length=255):
        super().__init__(primary_key, nullable)
        self._type = f"varchar({max_length})"
