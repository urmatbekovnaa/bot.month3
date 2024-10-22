import sqlite3


class Database:
    def __init__(self, path):
        self.path = path


    def create_table(self):
        with sqlite3.connect(self.path) as connection:
            connection.execute("""
            CREATE TABLE IF NOT EXISTS rewies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                visit_date TEXT,
                food_rating INTEGER,
                cleanliness_rating INTEGER,
                extra_comments TEXT
            )
            """)

            connection.execute("""
            CREATE TABLE IF NOT EXISTS foods(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VERCHAR(40),
                category VERCHAR(40),
                price INTEGER,
                weight FLOAT
            
            )
            """)

            connection.commit()


    def execute(self, query: str, params: tuple = None):
        with sqlite3.connect(self.path) as connection:
            connection.execute(query, params)
            connection.commit()
