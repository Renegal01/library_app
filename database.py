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


def get_books():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            author,
            publication_year,
            genre,
            total_copies,
            available_copies
        FROM books
        ORDER BY title
    """)

    books = cursor.fetchall()
    connection.close()

    return books


def add_book(title, author, publication_year, genre, total_copies):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO books (
            title,
            author,
            publication_year,
            genre,
            total_copies,
            available_copies
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        author,
        publication_year,
        genre,
        total_copies,
        total_copies
    ))

    connection.commit()
    connection.close()


def update_book(
        book_id,
        title,
        author,
        publication_year,
        genre,
        total_copies
):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT total_copies, available_copies
        FROM books
        WHERE id = ?
    """, (book_id,))

    book = cursor.fetchone()

    if book is None:
        connection.close()
        raise ValueError("Книга не найдена.")

    old_total_copies = book[0]
    old_available_copies = book[1]

    issued_copies = old_total_copies - old_available_copies

    if total_copies < issued_copies:
        connection.close()
        raise ValueError(
            "Количество экземпляров нельзя сделать меньше "
            "количества уже выданных книг."
        )

    new_available_copies = total_copies - issued_copies

    cursor.execute("""
        UPDATE books
        SET
            title = ?,
            author = ?,
            publication_year = ?,
            genre = ?,
            total_copies = ?,
            available_copies = ?
        WHERE id = ?
    """, (
        title,
        author,
        publication_year,
        genre,
        total_copies,
        new_available_copies,
        book_id
    ))

    connection.commit()
    connection.close()


def delete_book(book_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM books
            WHERE id = ?
        """, (book_id,))

        connection.commit()

    except sqlite3.IntegrityError as error:
        raise ValueError(
            "Книгу нельзя удалить, потому что она используется "
            "в истории выдач."
        ) from error

    finally:
        connection.close()


def get_readers():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            full_name,
            phone,
            email
        FROM readers
        ORDER BY full_name
    """)

    readers = cursor.fetchall()
    connection.close()

    return readers


def add_reader(full_name, phone, email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO readers (
            full_name,
            phone,
            email
        )
        VALUES (?, ?, ?)
    """, (
        full_name,
        phone,
        email
    ))

    connection.commit()
    connection.close()


def update_reader(reader_id, full_name, phone, email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE readers
        SET
            full_name = ?,
            phone = ?,
            email = ?
        WHERE id = ?
    """, (
        full_name,
        phone,
        email,
        reader_id
    ))

    connection.commit()
    connection.close()


def delete_reader(reader_id):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM readers
            WHERE id = ?
        """, (reader_id,))

        connection.commit()

    except sqlite3.IntegrityError as error:
        raise ValueError(
            "Читателя нельзя удалить, потому что он используется "
            "в истории выдач."
        ) from error

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()
    print("База данных успешно создана.")