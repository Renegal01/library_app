import tkinter as tk
from tkinter import ttk
from database import initialize_database
from books_view import BooksView
from readers_view import ReadersView
from loans_view import LoansView
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
    readers_tab = ReadersView(notebook)
    loans_tab = LoansView(notebook)
    notebook.add(
        books_tab,
        text="Книги"
    )
    notebook.add(
        readers_tab,
        text="Читатели"
    )
    notebook.add(
        loans_tab,
        text="Выдача книг"
    )
    def on_tab_changed(event):
        selected_tab = event.widget.select()
        tab_text = event.widget.tab(
            selected_tab,
            "text"
        )
        if tab_text == "Книги":
            books_tab.refresh_books()
        elif tab_text == "Читатели":
            readers_tab.refresh_readers()
        elif tab_text == "Выдача книг":
            loans_tab.refresh_data()
    notebook.bind(
        "<<NotebookTabChanged>>",
        on_tab_changed
    )
    root.mainloop()
if __name__ == "__main__":
    main()