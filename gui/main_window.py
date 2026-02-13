"""Main application window with menu, weight form, and graph."""
import tkinter as tk
from tkinter import messagebox

from config import APP_NAME, APP_VERSION
from db import add_weight, ensure_db
from gui.graph_display import GraphDisplay
from gui.weight_form import WeightForm


class MainWindow:
    """Main window: menu bar, weight form, graph."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.minsize(500, 400)
        self.root.geometry("700x500")

        self._build_menu()
        self._build_content()

    def _build_menu(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Close", command=self._on_close)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._on_about)

    def _build_content(self) -> None:
        form = WeightForm(self.root, on_add=self._on_weight_added)
        form.pack(pady=8, padx=8, fill=tk.X)

        self.graph = GraphDisplay(self.root)
        self.graph.pack(pady=8, padx=8, fill=tk.BOTH, expand=True)

    def _on_weight_added(self, weight: float) -> None:
        add_weight(weight)
        self.graph.refresh()

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
