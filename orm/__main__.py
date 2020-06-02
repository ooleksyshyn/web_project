from orm.model.model import Model
from orm.column.columns import IntegerColumn, StringColumn
from orm.model.database_connection import DataBaseConnection


class Student(Model):
    _connection = DataBaseConnection("localhost", "oleksii", "1", "testdb")
    id = IntegerColumn(primary_key=True)
    name = StringColumn()
    surname = StringColumn(nullable=False)


class Mob(Model):
    _connection = DataBaseConnection("localhost", "oleksii", "1", "testdb")
    id = IntegerColumn(primary_key=True, nullable=False)
    name = StringColumn(max_length=30)
    hp = IntegerColumn(nullable=False)


if __name__ == "__main__":
    for i in Mob.select("id", "name", expression=(Mob.hp > 50) & (Mob.id <= 1)):
        print(i)
