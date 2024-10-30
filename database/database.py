import sqlite3


class Database:
    def __init__(self, path):
        self.path = path


    def create_table(self):
        with sqlite3.connect(self.path) as connection:
            connection.execute("""
                        CREATE TABLE IF NOT EXISTS survey_rewies (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            phone TEXT,
                            visit_date TEXT,
                            food_rating INTEGER,
                            cleanliness_rating INTEGER,
                            extra_comments TEXT,
                            tg_id INTEGER
                        )
                        """)

            connection.execute("""
                     CREATE TABLE IF NOT EXISTS categories(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     category_name TEXT UNIQUE
                     )
                     """)

            connection.execute("""
            CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT 
            )
            """)

            connection.execute("""
            CREATE TABLE IF NOT EXISTS dishes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VERCHAR(40),
            price INTEGER,
            weight FLOAT,
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES categories(id)
            )
            """)

            connection.commit()


    def execute(self, query: str, params: tuple = None):
        with sqlite3.connect(self.path) as connection:
            connection.execute(query, params)
            connection.commit()


    def fetch(self, query: str, params: tuple = tuple()):
        with sqlite3.connect(self.path) as conn:
            result = conn.execute(query, params)
            result.row_factory = sqlite3.Row

            data = result.fetchall()
            return [dict(row) for row in data]
