import tkinter as tk

from database import initialize_database

def main():
    initialize_database()

    root = tk.Tk()
    root.title("Библиотека")
    root.geometry("900x600")

    title_label = tk.Label(
        root,
        text="Библиотека",
        font=("Arial", 24)
    )
    title_label.pack(pady=30)

    root.mainloop()

if __name__ == "__main__":
    main()