"""Main application window with menu, weight/water/distance forms, graph and table views."""
import tkinter as tk
from tkinter import messagebox

from config import APP_NAME, APP_VERSION
from db import add_weight, add_water, add_distance, ensure_db, get_user_profile
from gui.user_profile_form import UserProfileForm
from gui.weight_form import WeightForm
from gui.weight_graph_display import WeightGraphDisplay
from gui.weight_table_display import WeightTableDisplay
from gui.water_form import WaterForm
from gui.water_graph_display import WaterGraphDisplay
from gui.water_table_display import WaterTableDisplay
from gui.distance_form import DistanceForm
from gui.distance_graph_display import DistanceGraphDisplay
from gui.distance_table_display import DistanceTableDisplay


class MainWindow:
    """Main window: menu bar, weight/water/distance forms, and switchable graph/table view per metric."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.minsize(500, 400)
        self.root.geometry("700x500")

        self._build_menu()
        self._build_content()
        self._current_metric: str = "weight"
        self._current_view: str = "graph"

    def _build_menu(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Settings...", command=self._on_settings)
        file_menu.add_command(label="Close", command=self._on_close)

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Weight", command=lambda: self._switch_metric("weight"))
        view_menu.add_command(label="Water", command=lambda: self._switch_metric("water"))
        view_menu.add_command(label="Distance", command=lambda: self._switch_metric("distance"))
        view_menu.add_separator()
        view_menu.add_command(label="Graph", command=lambda: self._switch_view("graph"))
        view_menu.add_command(label="Table", command=lambda: self._switch_view("table"))

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._on_about)

    def _build_content(self) -> None:
        form_row = tk.Frame(self.root)
        form_row.pack(pady=8, padx=8, fill=tk.X)
        self.weight_form = WeightForm(form_row, on_add=self._on_weight_added)
        self.weight_form.pack(side=tk.LEFT)
        self.water_form = WaterForm(form_row, on_add=self._on_water_added)
        self.water_form.pack(side=tk.LEFT)
        self.water_form.pack_forget()
        self.distance_form = DistanceForm(form_row, on_add=self._on_distance_added)
        self.distance_form.pack(side=tk.LEFT)
        self.distance_form.pack_forget()

        self.delete_btn = tk.Button(form_row, text="Delete", command=self._on_delete_selected)
        self.delete_btn.pack(side=tk.RIGHT)
        self.delete_btn.pack_forget()

        self.content = tk.Frame(self.root)
        self.content.pack(pady=8, padx=8, fill=tk.BOTH, expand=True)

        pack_opts = {"fill": tk.BOTH, "expand": True}

        self.weight_graph = WeightGraphDisplay(self.content)
        self.weight_table = WeightTableDisplay(self.content, on_row_deleted=self.weight_graph.refresh)
        self.water_graph = WaterGraphDisplay(self.content)
        self.water_table = WaterTableDisplay(self.content, on_row_deleted=self.water_graph.refresh)
        self.distance_graph = DistanceGraphDisplay(self.content)
        self.distance_table = DistanceTableDisplay(self.content, on_row_deleted=self.distance_graph.refresh)

        self.weight_graph.pack(**pack_opts)
        self._pack_opts = pack_opts

    def _switch_metric(self, metric: str) -> None:
        if metric == self._current_metric:
            return
        self._current_metric = metric
        self.weight_form.pack_forget()
        self.water_form.pack_forget()
        self.distance_form.pack_forget()
        if metric == "weight":
            self.weight_form.pack(side=tk.LEFT)
        elif metric == "water":
            self.water_form.pack(side=tk.LEFT)
        else:
            self.distance_form.pack(side=tk.LEFT)
        self._show_content()

    def _switch_view(self, view: str) -> None:
        if view == self._current_view:
            return
        self._current_view = view
        self._show_content()

    def _show_content(self) -> None:
        """Show the graph or table for the current metric; show/hide Delete for table view."""
        opts = self._pack_opts
        self.weight_graph.pack_forget()
        self.weight_table.pack_forget()
        self.water_graph.pack_forget()
        self.water_table.pack_forget()
        self.distance_graph.pack_forget()
        self.distance_table.pack_forget()

        if self._current_view == "graph":
            self.delete_btn.pack_forget()
            if self._current_metric == "weight":
                self.weight_graph.pack(**opts)
                self.root.update_idletasks()
                self.weight_graph.refresh()
            elif self._current_metric == "water":
                self.water_graph.pack(**opts)
                self.root.update_idletasks()
                self.water_graph.refresh()
            else:
                self.distance_graph.pack(**opts)
                self.root.update_idletasks()
                self.distance_graph.refresh()
        else:
            if self._current_metric == "weight":
                self.weight_table.pack(**opts)
                self.weight_table.refresh()
            elif self._current_metric == "water":
                self.water_table.pack(**opts)
                self.water_table.refresh()
            else:
                self.distance_table.pack(**opts)
                self.distance_table.refresh()
            self.delete_btn.pack(side=tk.RIGHT)

    def _on_delete_selected(self) -> None:
        if self._current_metric == "weight":
            self.weight_table.delete_selected_row()
        elif self._current_metric == "water":
            self.water_table.delete_selected_row()
        else:
            self.distance_table.delete_selected_row()

    def _on_weight_added(self, weight: float) -> None:
        add_weight(weight)
        self.weight_graph.refresh()
        self.weight_table.refresh()

    def _on_water_added(self, ounces: float) -> None:
        add_water(ounces)
        self.water_graph.refresh()
        self.water_table.refresh()

    def _on_distance_added(self, miles: float) -> None:
        add_distance(miles)
        self.distance_graph.refresh()
        self.distance_table.refresh()

    def _on_settings(self) -> None:
        """Open the user profile (Settings) dialog."""
        UserProfileForm(self.root, title="Settings – User profile")

    def _on_close(self) -> None:
        self.root.quit()

    def _on_about(self) -> None:
        messagebox.showinfo(
            "About",
            f"{APP_NAME}\nVersion {APP_VERSION}",
        )

    def run(self) -> None:
        ensure_db()
        if get_user_profile() is None:
            form = UserProfileForm(self.root, title="User profile – Please enter your details")
            form.dialog.lift()
            form.dialog.focus_force()
            self.root.wait_window(form.dialog)
        self._bring_to_foreground()
        self.root.mainloop()

    def _bring_to_foreground(self) -> None:
        """Raise the window to the front and give it focus when the app starts."""
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(100, lambda: self.root.attributes("-topmost", False))
        self.root.focus_force()


def run_app() -> None:
    """Create and run the main window."""
    ensure_db()
    app = MainWindow()
    app.run()
