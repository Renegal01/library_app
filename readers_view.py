import tkinter as tk
from tkinter import ttk, messagebox

from database import (
    get_readers,
    add_reader,
    update_reader,
    delete_reader
)


class ReaderDialog(tk.Toplevel):
    def __init__(self, parent, window_title, initial_values=None):
        super().__init__(parent)

        self.result = None
        self.title(window_title)
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        if initial_values is None:
            initial_values = {}

        self.full_name_var = tk.StringVar(
            value=initial_values.get("full_name", "")
        )

        self.phone_var = tk.StringVar(
            value=initial_values.get("phone", "")
        )

        self.email_var = tk.StringVar(
            value=initial_values.get("email", "")
        )

        self.create_widgets()

        self.bind("<Return>", lambda event: self.save())
        self.bind("<Escape>", lambda event: self.destroy())

        self.after(100, self.full_name_entry.focus_set)

    def create_widgets(self):
        content_frame = ttk.Frame(self, padding=20)
        content_frame.grid(row=0, column=0)

        ttk.Label(
            content_frame,
            text="ФИО:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        self.full_name_entry = ttk.Entry(
            content_frame,
            textvariable=self.full_name_var,
            width=40
        )
        self.full_name_entry.grid(
            row=0,
            column=1,
            pady=7
        )

        ttk.Label(
            content_frame,
            text="Телефон:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        ttk.Entry(
            content_frame,
            textvariable=self.phone_var,
            width=40
        ).grid(
            row=1,
            column=1,
            pady=7
        )

        ttk.Label(
            content_frame,
            text="Электронная почта:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=7
        )

        ttk.Entry(
            content_frame,
            textvariable=self.email_var,
            width=40
        ).grid(
            row=2,
            column=1,
            pady=7
        )

        buttons_frame = ttk.Frame(content_frame)
        buttons_frame.grid(
            row=3,
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
        full_name = self.full_name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()

        if not full_name:
            messagebox.showwarning(
                "Проверка данных",
                "Введите ФИО читателя.",
                parent=self
            )
            return

        self.result = {
            "full_name": full_name,
            "phone": phone,
            "email": email
        }

        self.destroy()


class ReadersView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=15)

        self.create_widgets()
        self.refresh_readers()

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
            "full_name",
            "phone",
            "email"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        self.tree.heading(
            "full_name",
            text="ФИО"
        )
        self.tree.heading(
            "phone",
            text="Телефон"
        )
        self.tree.heading(
            "email",
            text="Электронная почта"
        )

        self.tree.column(
            "full_name",
            width=280
        )
        self.tree.column(
            "phone",
            width=180
        )
        self.tree.column(
            "email",
            width=250
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
            lambda event: self.edit_reader()
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
            command=self.add_reader
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ttk.Button(
            buttons_frame,
            text="Редактировать",
            command=self.edit_reader
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ttk.Button(
            buttons_frame,
            text="Удалить",
            command=self.delete_reader
        ).pack(
            side="left"
        )

    def refresh_readers(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        readers = get_readers()

        for reader in readers:
            reader_id = reader[0]

            values = (
                reader[1],
                reader[2] if reader[2] is not None else "",
                reader[3] if reader[3] is not None else ""
            )

            self.tree.insert(
                "",
                tk.END,
                iid=str(reader_id),
                values=values
            )

    def get_selected_reader_id(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "Выбор читателя",
                "Сначала выберите читателя в таблице."
            )
            return None

        return int(selected[0])

    def add_reader(self):
        dialog = ReaderDialog(
            self,
            "Добавление читателя"
        )

        self.wait_window(dialog)

        if dialog.result is None:
            return

        add_reader(**dialog.result)
        self.refresh_readers()

    def edit_reader(self):
        reader_id = self.get_selected_reader_id()

        if reader_id is None:
            return

        item = self.tree.item(str(reader_id))
        values = item["values"]

        initial_values = {
            "full_name": values[0],
            "phone": values[1],
            "email": values[2]
        }

        dialog = ReaderDialog(
            self,
            "Редактирование читателя",
            initial_values
        )

        self.wait_window(dialog)

        if dialog.result is None:
            return

        update_reader(
            reader_id=reader_id,
            **dialog.result
        )

        self.refresh_readers()

    def delete_reader(self):
        reader_id = self.get_selected_reader_id()

        if reader_id is None:
            return

        item = self.tree.item(str(reader_id))
        full_name = item["values"][0]

        confirmed = messagebox.askyesno(
            "Удаление читателя",
            f"Удалить читателя «{full_name}»?"
        )

        if not confirmed:
            return

        try:
            delete_reader(reader_id)

        except ValueError as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )
            return

        self.refresh_readers()