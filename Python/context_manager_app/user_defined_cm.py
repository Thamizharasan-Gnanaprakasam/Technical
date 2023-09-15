import sqlite3 as sql
class SQL_Connection:
    def __init__(self,host):
        self.connection = None
        self.cursor = None
        self.host = host

    def __enter__(self):
        self.connection = sql.connect(database=self.host)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()
