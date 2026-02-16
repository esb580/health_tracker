"""Distance (miles) input form widget."""
import tkinter as tk
from tkinter import messagebox
from typing import Callable


class DistanceForm(tk.Frame):
    """A form with distance (miles) entry and Add button."""

    def __init__(
        self,
        parent: tk.Misc,
        on_add: Callable[[float], None] | None = None,
        **kwargs: object,
    ) -> None:
        super().__init__(parent, **kwargs)
        self.on_add = on_add

        tk.Label(self, text="Miles:").pack(side=tk.LEFT, padx=(0, 4))
        self.entry = tk.Entry(self, width=10)
        self.entry.pack(side=tk.LEFT, padx=(0, 8))
        self.entry.bind("<Return>", lambda e: self._submit())

        tk.Button(self, text="Add", command=self._submit).pack(side=tk.LEFT)

    def _submit(self) -> None:
        try:
            text = self.entry.get().strip()
            if not text:
                return
            value = float(text)
            if value <= 0 or value > 999.99:
                messagebox.showerror("Invalid amount", "Enter miles between 0 and 999.99")
                return
            if self.on_add:
                self.on_add(value)
            self.entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a number (e.g. 2.5)")
