import tkinter as tk
from tkinter import ttk

from database import initialize_database
from books_view import BooksView


def main():
    initialize_database()

    root = tk.Tk()
    root.title("Библиотека")
    root.geometry("1000x650")
    root.minsize(850, 500)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)

    title_label = ttk.Label(
        root,
        text="Библиотека",
        font=("Arial", 24)
    )

    title_label.grid(
        row=0,
        column=0,
        pady=(20, 10)
    )

    notebook = ttk.Notebook(root)

    notebook.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=20,
        pady=(0, 20)
    )

    books_tab = BooksView(notebook)

    notebook.add(
        books_tab,
        text="Книги"
    )

    root.mainloop()


if __name__ == "__main__":
    main()