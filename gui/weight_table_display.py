"""Table display widget for weight history."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from typing import Callable

from db import get_weight_entries, delete_weight


def delete_selected_row(tree: ttk.Treeview, on_deleted: Callable[[], None] | None = None) -> bool:
    """
    Delete the selected row from the tree and the database.
    Returns True if a row was deleted, False if no selection.
    Calls on_deleted() after a successful delete (e.g. to refresh graph).
    """
    selection = tree.selection()
    if not selection:
        messagebox.showinfo("No selection", "Select a row to delete.")
        return False
    iid = selection[0]
    try:
        entry_id = int(iid)
    except ValueError:
        messagebox.showerror("Error", "Could not identify row.")
        return False
    delete_weight(entry_id)
    tree.delete(iid)
    if on_deleted:
        on_deleted()
    return True


class WeightTableDisplay(tk.Frame):
    """A frame that shows weight history in an autosized table."""

    def __init__(
        self,
        parent: tk.Misc,
        on_row_deleted: Callable[[], None] | None = None,
        **kwargs: object,
    ) -> None:
        super().__init__(parent, **kwargs)
        self.on_row_deleted = on_row_deleted

        # Treeview with scrollbar; use id as iid for deletion
        self.tree = ttk.Treeview(self, columns=("date", "weight"), show="headings", height=20)
        self.tree.heading("date", text="Date")
        self.tree.heading("weight", text="Weight")
        self.tree.column("date", minwidth=120, stretch=True)
        self.tree.column("weight", minwidth=80, stretch=True)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.refresh()

    def refresh(self) -> None:
        """Reload data from DB and repopulate the table."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for entry_id, created_at, weight in get_weight_entries():
            date_str = created_at.strftime("%Y-%m-%d %H:%M") if isinstance(created_at, datetime) else str(created_at)
            self.tree.insert("", tk.END, iid=str(entry_id), values=(date_str, f"{weight:.2f}"))

    def delete_selected_row(self) -> bool:
        """Delete the currently selected row from the table and DB. Returns True if deleted."""
        return delete_selected_row(self.tree, on_deleted=self._after_delete)

    def _after_delete(self) -> None:
        """Called after a row is deleted; refresh graph if callback set."""
        if self.on_row_deleted:
            self.on_row_deleted()
