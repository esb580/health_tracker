"""Graph display widget for water (ounces) using matplotlib embedded in tkinter."""
import tkinter as tk
from typing import TYPE_CHECKING

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

if TYPE_CHECKING:
    from matplotlib.axes import Axes

from db import get_water_history


class WaterGraphDisplay(tk.Frame):
    """A frame that shows water (ounces) over time in a matplotlib graph."""

    def __init__(self, parent: tk.Misc, **kwargs: object) -> None:
        super().__init__(parent, **kwargs)
        self.figure = Figure(figsize=(6, 3), dpi=100)
        self.ax: Axes = self.figure.add_subplot(111)
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Ounces")
        self.ax.grid(True, alpha=0.3)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.refresh()

    def refresh(self) -> None:
        """Reload data from DB and redraw the graph."""
        history = get_water_history()
        self.ax.clear()
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Ounces")
        self.ax.grid(True, alpha=0.3)
        if history:
            dates = [d for d, _ in history]
            ounces = [o for _, o in history]
            self.ax.plot(dates, ounces, "o-", markersize=4)
            self.ax.xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
            self.figure.autofmt_xdate()
        self.canvas.draw()
