import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox

from database import (
    get_available_books,
    get_readers,
    add_loan,
    get_active_loans
)


class LoansView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        self.book_ids = {}
        self.reader_ids = {}

        self.create_widgets()
        self.refresh_data()

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        issue_frame = ttk.LabelFrame(
            self,
            text="Новая выдача",
            padding=15
        )

        issue_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 15)
        )

        issue_frame.columnconfigure(1, weight=1)

        ttk.Label(
            issue_frame,
            text="Книга:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.book_combobox = ttk.Combobox(
            issue_frame,
            state="readonly",
            width=60
        )

        self.book_combobox.grid(
            row=0,
            column=1,
            sticky="ew",
            pady=7
        )

        ttk.Label(
            issue_frame,
            text="Читатель:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.reader_combobox = ttk.Combobox(
            issue_frame,
            state="readonly",
            width=60
        )

        self.reader_combobox.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=7
        )

        ttk.Button(
            issue_frame,
            text="Выдать книгу",
            command=self.issue_book
        ).grid(
            row=2,
            column=0,
            columnspan=2,
            pady=(10, 0)
        )

        table_frame = ttk.LabelFrame(
            self,
            text="Активные выдачи",
            padding=10
        )

        table_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = (
            "book",
            "author",
            "reader",
            "issue_date"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.tree.heading(
            "book",
            text="Книга"
        )

        self.tree.heading(
            "author",
            text="Автор"
        )

        self.tree.heading(
            "reader",
            text="Читатель"
        )

        self.tree.heading(
            "issue_date",
            text="Дата выдачи"
        )

        self.tree.column(
            "book",
            width=250
        )

        self.tree.column(
            "author",
            width=180
        )

        self.tree.column(
            "reader",
            width=220
        )

        self.tree.column(
            "issue_date",
            width=110,
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

    def refresh_data(self):
        self.refresh_books()
        self.refresh_readers()
        self.refresh_loans()

    def refresh_books(self):
        books = get_available_books()

        self.book_ids = {}
        values = []

        for book in books:
            book_id = book[0]
            title = book[1]
            author = book[2]
            available = book[3]

            display_value = (
                f"{book_id}: {title} — {author} "
                f"(доступно: {available})"
            )

            self.book_ids[display_value] = book_id
            values.append(display_value)

        self.book_combobox["values"] = values

        if values:
            self.book_combobox.current(0)
        else:
            self.book_combobox.set("")

    def refresh_readers(self):
        readers = get_readers()

        self.reader_ids = {}
        values = []

        for reader in readers:
            reader_id = reader[0]
            full_name = reader[1]

            display_value = (
                f"{reader_id}: {full_name}"
            )

            self.reader_ids[display_value] = reader_id
            values.append(display_value)

        self.reader_combobox["values"] = values

        if values:
            self.reader_combobox.current(0)
        else:
            self.reader_combobox.set("")

    def refresh_loans(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        loans = get_active_loans()

        for loan in loans:
            loan_id = loan[0]
            book_title = loan[1]
            author = loan[2]
            reader = loan[3]
            issue_date = loan[4]

            formatted_date = self.format_date(issue_date)

            self.tree.insert(
                "",
                tk.END,
                iid=str(loan_id),
                values=(
                    book_title,
                    author,
                    reader,
                    formatted_date
                )
            )

    def issue_book(self):
        book_value = self.book_combobox.get()
        reader_value = self.reader_combobox.get()

        if not book_value:
            messagebox.showwarning(
                "Выдача книги",
                "Нет доступной книги для выдачи."
            )
            return

        if not reader_value:
            messagebox.showwarning(
                "Выдача книги",
                "Сначала добавьте хотя бы одного читателя."
            )
            return

        book_id = self.book_ids.get(book_value)
        reader_id = self.reader_ids.get(reader_value)

        if book_id is None or reader_id is None:
            messagebox.showerror(
                "Ошибка",
                "Не удалось определить книгу или читателя."
            )
            return

        today = date.today().isoformat()

        try:
            add_loan(
                book_id=book_id,
                reader_id=reader_id,
                issue_date=today
            )

        except ValueError as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )
            self.refresh_data()
            return

        messagebox.showinfo(
            "Выдача книги",
            "Книга успешно выдана."
        )

        self.refresh_data()

    @staticmethod
    def format_date(date_value):
        if not date_value:
            return ""

        parts = date_value.split("-")

        if len(parts) != 3:
            return date_value

        return f"{parts[2]}.{parts[1]}.{parts[0]}"