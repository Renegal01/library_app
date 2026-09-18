import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

from database import (
    get_books,
    add_book,
    update_book,
    delete_book
)


class BookDialog(tk.Toplevel):
    def __init__(self, parent, window_title, initial_values=None):
        super().__init__(parent)

        self.result = None
        self.title(window_title)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        if initial_values is None:
            initial_values = {}

        self.title_var = tk.StringVar(
            value=initial_values.get("title", "")
        )

        self.author_var = tk.StringVar(
            value=initial_values.get("author", "")
        )

        self.year_var = tk.StringVar(
            value=initial_values.get("publication_year", "")
        )

        self.genre_var = tk.StringVar(
            value=initial_values.get("genre", "")
        )

        self.copies_var = tk.StringVar(
            value=initial_values.get("total_copies", "1")
        )

        self.create_widgets()

        self.bind("<Return>", lambda event: self.save())
        self.bind("<Escape>", lambda event: self.destroy())

        self.after(100, self.title_entry.focus_set)

    def create_widgets(self):
        content_frame = ttk.Frame(self, padding=20)
        content_frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(
            content_frame,
            text="Название:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.title_entry = ttk.Entry(
            content_frame,
            textvariable=self.title_var,
            width=40
        )
        self.title_entry.grid(
            row=0,
            column=1,
            pady=7
        )

        ttk.Label(
            content_frame,
            text="Автор:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        ttk.Entry(
            content_frame,
            textvariable=self.author_var,
            width=40
        ).grid(
            row=1,
            column=1,
            pady=7
        )

        ttk.Label(
            content_frame,
            text="Год издания:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        ttk.Entry(
            content_frame,
            textvariable=self.year_var,
            width=40
        ).grid(
            row=2,
            column=1,
            pady=7
        )

        ttk.Label(
            content_frame,
            text="Жанр:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        ttk.Entry(
            content_frame,
            textvariable=self.genre_var,
            width=40
        ).grid(
            row=3,
            column=1,
            pady=7
        )

        ttk.Label(
            content_frame,
            text="Количество экземпляров:"
        ).grid(
            row=4,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        ttk.Entry(
            content_frame,
            textvariable=self.copies_var,
            width=40
        ).grid(
            row=4,
            column=1,
            pady=7
        )

        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=(20, 0)
        )

        ttk.Button(
            buttons_frame,
            text="Сохранить",
            command=self.save
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            buttons_frame,
            text="Отмена",
            command=self.destroy
        ).pack(
            side="left",
            padx=5
        )

    def save(self):
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        year_text = self.year_var.get().strip()
        genre = self.genre_var.get().strip()
        copies_text = self.copies_var.get().strip()

        if not title:
            messagebox.showwarning(
                "Проверка данных",
                "Введите название книги.",
                parent=self
            )
            return

        if not author:
            messagebox.showwarning(
                "Проверка данных",
                "Введите автора книги.",
                parent=self
            )
            return

        publication_year = None

        if year_text:
            try:
                publication_year = int(year_text)

            except ValueError:
                messagebox.showwarning(
                    "Проверка данных",
                    "Год издания должен быть целым числом.",
                    parent=self
                )
                return

            current_year = datetime.now().year

            if publication_year < 1 or publication_year > current_year:
                messagebox.showwarning(
                    "Проверка данных",
                    f"Укажите год от 1 до {current_year}.",
                    parent=self
                )
                return

        try:
            total_copies = int(copies_text)

        except ValueError:
            messagebox.showwarning(
                "Проверка данных",
                "Количество экземпляров должно быть целым числом.",
                parent=self
            )
            return

        if total_copies < 1:
            messagebox.showwarning(
                "Проверка данных",
                "Количество экземпляров должно быть больше нуля.",
                parent=self
            )
            return

        self.result = {
            "title": title,
            "author": author,
            "publication_year": publication_year,
            "genre": genre,
            "total_copies": total_copies
        }

        self.destroy()


class BooksView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        self.create_widgets()
        self.refresh_books()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        table_frame = ttk.Frame(self)
        table_frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = (
            "title",
            "author",
            "year",
            "genre",
            "total",
            "available"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading(
            "title",
            text="Название"
        )
        self.tree.heading(
            "author",
            text="Автор"
        )
        self.tree.heading(
            "year",
            text="Год"
        )
        self.tree.heading(
            "genre",
            text="Жанр"
        )
        self.tree.heading(
            "total",
            text="Всего"
        )
        self.tree.heading(
            "available",
            text="Доступно"
        )

        self.tree.column(
            "title",
            width=230
        )
        self.tree.column(
            "author",
            width=180
        )
        self.tree.column(
            "year",
            width=80,
            anchor="center"
        )
        self.tree.column(
            "genre",
            width=130
        )
        self.tree.column(
            "total",
            width=80,
            anchor="center"
        )
        self.tree.column(
            "available",
            width=90,
            anchor="center"
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        self.tree.bind(
            "<Double-1>",
            lambda event: self.edit_book()
        )

        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(
            row=1,
            column=0,
            sticky="w",
            pady=(15, 0)
        )

        ttk.Button(
            buttons_frame,
            text="Добавить",
            command=self.add_book
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ttk.Button(
            buttons_frame,
            text="Редактировать",
            command=self.edit_book
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ttk.Button(
            buttons_frame,
            text="Удалить",
            command=self.delete_book
        ).pack(
            side="left"
        )

    def refresh_books(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        books = get_books()

        for book in books:
            book_id = book[0]

            values = (
                book[1],
                book[2],
                book[3] if book[3] is not None else "",
                book[4] if book[4] is not None else "",
                book[5],
                book[6]
            )

            self.tree.insert(
                "",
                tk.END,
                iid=str(book_id),
                values=values
            )

    def get_selected_book_id(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Выбор книги",
                "Сначала выберите книгу в таблице."
            )
            return None

        return int(selected[0])

    def add_book(self):
        dialog = BookDialog(
            self,
            "Добавление книги"
        )

        self.wait_window(dialog)

        if dialog.result is None:
            return

        add_book(**dialog.result)
        self.refresh_books()

    def edit_book(self):
        book_id = self.get_selected_book_id()

        if book_id is None:
            return

        item = self.tree.item(str(book_id))
        values = item["values"]

        initial_values = {
            "title": values[0],
            "author": values[1],
            "publication_year": values[2],
            "genre": values[3],
            "total_copies": values[4]
        }

        dialog = BookDialog(
            self,
            "Редактирование книги",
            initial_values
        )

        self.wait_window(dialog)

        if dialog.result is None:
            return

        try:
            update_book(
                book_id=book_id,
                **dialog.result
            )

        except ValueError as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )
            return

        self.refresh_books()

    def delete_book(self):
        book_id = self.get_selected_book_id()

        if book_id is None:
            return

        item = self.tree.item(str(book_id))
        book_title = item["values"][0]

        confirmed = messagebox.askyesno(
            "Удаление книги",
            f"Удалить книгу «{book_title}»?"
        )

        if not confirmed:
            return

        try:
            delete_book(book_id)

        except ValueError as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )
            return

        self.refresh_books()