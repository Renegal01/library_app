import sqlite3
DATABASE_NAME = "library.db"
def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publication_year INTEGER,
            genre TEXT,
            total_copies INTEGER NOT NULL DEFAULT 1,
            available_copies INTEGER NOT NULL DEFAULT 1,
            CHECK (total_copies >= 0),
            CHECK (
                available_copies >= 0
                AND available_copies <= total_copies
            )
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            phone TEXT,
            email TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            reader_id INTEGER NOT NULL,
            issue_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT NOT NULL DEFAULT 'Выдана',
            FOREIGN KEY (book_id) REFERENCES books (id),
            FOREIGN KEY (reader_id) REFERENCES readers (id)
        )
    """)
    connection.commit()
    connection.close()
if __name__ == "__main__":
    initialize_database()
