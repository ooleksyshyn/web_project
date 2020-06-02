import mysql.connector


class DataBaseConnection:
    def __init__(self, host, username, password, database):
        self.__connection = mysql.connector.connect(
            host=host,
            user=username,
            passwd=password,
            database=database
        )
        self.cursor = self.__connection.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        try:
            self.__connection.commit()
        except mysql.connector.errors.InternalError:
            pass

        return list(self.cursor)
