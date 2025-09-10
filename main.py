import tkinter as tk
from tkinter import ttk


class DatabaseWindow(tk.Toplevel):
    """Window displaying a placeholder Excel-like table."""

    def __init__(self, master):
        super().__init__(master)
        self.title("Base de Datos")
        self.geometry("600x400")
        self.configure(padx=10, pady=10)

        self.tree = ttk.Treeview(
            self, columns=("ID", "Nombre", "Valor"), show="headings"
        )
        for col in ("ID", "Nombre", "Valor"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)
        self.tree.pack(expand=True, fill=tk.BOTH)

        sample_data = [
            (1, "Elemento A", 10),
            (2, "Elemento B", 20),
            (3, "Elemento C", 30),
        ]
        for row in sample_data:
            self.tree.insert("", tk.END, values=row)

        self.tree.bind("<Double-1>", self._on_double_click)
        self._edit_box = None

    def _on_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        column = self.tree.identify_column(event.x)
        row = self.tree.identify_row(event.y)
        if not row:
            return
        x, y, width, height = self.tree.bbox(row, column)
        item = self.tree.item(row)
        value_index = int(column.replace("#", "")) - 1
        current_value = item["values"][value_index]

        self._edit_box = tk.Entry(self.tree)
        self._edit_box.insert(0, current_value)
        self._edit_box.place(x=x, y=y, width=width, height=height)
        self._edit_box.focus()
        self._edit_box.bind("<Return>", lambda e: self._save_edit(row, column))
        self._edit_box.bind("<Escape>", lambda e: self._cancel_edit())
        self._edit_box.bind(
            "<FocusOut>", lambda e: self._save_edit(row, column)
        )

    def _save_edit(self, row, column):
        if self._edit_box is None:
            return
        new_value = self._edit_box.get()
        value_index = int(column.replace("#", "")) - 1
        values = list(self.tree.item(row, "values"))
        values[value_index] = new_value
        self.tree.item(row, values=values)
        self._edit_box.destroy()
        self._edit_box = None

    def _cancel_edit(self):
        if self._edit_box is not None:
            self._edit_box.destroy()
            self._edit_box = None


class ActionsWindow(tk.Toplevel):
    """Placeholder window for future actions."""

    def __init__(self, master):
        super().__init__(master)
        self.title("Acciones")
        self.geometry("400x200")
        self.configure(padx=20, pady=20)
        ttk.Label(
            self, text="Funciones de acciones por implementar."
        ).pack(expand=True)


class MainApp(tk.Tk):
    """Main application window with navigation."""

    def __init__(self):
        super().__init__()
        self.title("Interfaz Principal")
        self.geometry("300x200")
        self.configure(padx=20, pady=20)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", padding=6, font=("Segoe UI", 12))

        ttk.Label(
            self, text="Seleccione una opción", font=("Segoe UI", 14)
        ).pack(pady=(0, 20))

        ttk.Button(
            self, text="1: Ver Base de Datos", command=self.open_database
        ).pack(fill=tk.X, pady=5)
        ttk.Button(
            self, text="2: Acciones", command=self.open_actions
        ).pack(fill=tk.X, pady=5)

    def open_database(self):
        DatabaseWindow(self)

    def open_actions(self):
        ActionsWindow(self)


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
