"""Main application window with menu, weight form, graph and table views."""
import tkinter as tk
from tkinter import messagebox

from config import APP_NAME, APP_VERSION
from db import add_weight, ensure_db
from gui.graph_display import GraphDisplay
from gui.table_display import TableDisplay
from gui.weight_form import WeightForm


class MainWindow:
    """Main window: menu bar, weight form, and switchable graph/table view."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.minsize(500, 400)
        self.root.geometry("700x500")

        self._build_menu()
        self._build_content()
        self._current_view: str = "graph"

    def _build_menu(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Close", command=self._on_close)

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Graph", command=lambda: self._switch_view("graph"))
        view_menu.add_command(label="Table", command=lambda: self._switch_view("table"))

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._on_about)

    def _build_content(self) -> None:
        form_row = tk.Frame(self.root)
        form_row.pack(pady=8, padx=8, fill=tk.X)
        form = WeightForm(form_row, on_add=self._on_weight_added)
        form.pack(side=tk.LEFT)
        self.delete_btn = tk.Button(form_row, text="Delete", command=self._on_delete_selected)
        self.delete_btn.pack(side=tk.RIGHT)
        self.delete_btn.pack_forget()

        # Single content area so graph and table keep the same size when switching
        self.content = tk.Frame(self.root)
        self.content.pack(pady=8, padx=8, fill=tk.BOTH, expand=True)

        self.graph = GraphDisplay(self.content)
        self.table = TableDisplay(self.content, on_row_deleted=self.graph.refresh)
        self.graph.pack(fill=tk.BOTH, expand=True)
        # Table starts hidden; same pack options when shown
        self._table_pack_options = {"fill": tk.BOTH, "expand": True}
        self._graph_pack_options = {"fill": tk.BOTH, "expand": True}

    def _switch_view(self, view: str) -> None:
        if view == self._current_view:
            return
        self._current_view = view
        if view == "graph":
            self.delete_btn.pack_forget()
            self.table.pack_forget()
            self.graph.pack(**self._graph_pack_options)
            self.root.update_idletasks()
            self.graph.refresh()
        else:
            self.graph.pack_forget()
            self.table.pack(**self._table_pack_options)
            self.table.refresh()
            self.delete_btn.pack(side=tk.RIGHT)

    def _on_delete_selected(self) -> None:
        self.table.delete_selected_row()

    def _on_weight_added(self, weight: float) -> None:
        add_weight(weight)
        self.graph.refresh()
        self.table.refresh()

    def _on_close(self) -> None:
        self.root.quit()

    def _on_about(self) -> None:
        messagebox.showinfo(
            "About",
            f"{APP_NAME}\nVersion {APP_VERSION}",
        )

    def run(self) -> None:
        ensure_db()
        self.root.mainloop()


def run_app() -> None:
    """Create and run the main window."""
    app = MainWindow()
    app.run()
