"""User profile settings dialog (File → Settings)."""
import tkinter as tk
from tkinter import ttk, messagebox

from db import get_user_profile, save_user_profile
from user_profile import UserProfile


class UserProfileForm:
    """A Toplevel dialog to view and edit the user profile (name, gender, age, height)."""

    def __init__(self, parent: tk.Misc, title: str = "User profile") -> None:
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.geometry("340x220")
        self.dialog.resizable(False, False)

        frame = ttk.Frame(self.dialog, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="First name:").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.first_name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.first_name_var, width=28).grid(row=0, column=1, pady=4, padx=(8, 0))

        ttk.Label(frame, text="Last name:").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.last_name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.last_name_var, width=28).grid(row=1, column=1, pady=4, padx=(8, 0))

        ttk.Label(frame, text="Gender:").grid(row=2, column=0, sticky=tk.W, pady=4)
        self.gender_var = tk.StringVar()
        gender_combo = ttk.Combobox(
            frame, textvariable=self.gender_var, width=26,
            values=["", "Male", "Female", "Other"],
        )
        gender_combo.grid(row=2, column=1, pady=4, padx=(8, 0))

        ttk.Label(frame, text="Age:").grid(row=3, column=0, sticky=tk.W, pady=4)
        self.age_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.age_var, width=28).grid(row=3, column=1, pady=4, padx=(8, 0))

        ttk.Label(frame, text="Height (inches):").grid(row=4, column=0, sticky=tk.W, pady=4)
        self.height_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.height_var, width=28).grid(row=4, column=1, pady=4, padx=(8, 0))

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=16)
        ttk.Button(btn_frame, text="Save", command=self._save).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(btn_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT)

        self._load()

    def _load(self) -> None:
        """Load current profile from DB into the form."""
        profile = get_user_profile()
        if profile:
            self.first_name_var.set(profile.first_name)
            self.last_name_var.set(profile.last_name)
            self.gender_var.set(profile.gender)
            self.age_var.set(str(profile.age) if profile.age is not None else "")
            self.height_var.set(str(profile.height_inches) if profile.height_inches is not None else "")

    def _save(self) -> None:
        """Validate, save to DB, and close."""
        first = self.first_name_var.get().strip()
        last = self.last_name_var.get().strip()
        gender = self.gender_var.get().strip()
        age_str = self.age_var.get().strip()
        height_str = self.height_var.get().strip()

        age: int | None = None
        if age_str:
            try:
                age = int(age_str)
                if age < 0 or age > 150:
                    messagebox.showerror("Invalid age", "Enter an age between 0 and 150.")
                    return
            except ValueError:
                messagebox.showerror("Invalid age", "Please enter a whole number.")
                return

        height_inches: float | None = None
        if height_str:
            try:
                height_inches = float(height_str)
                if height_inches <= 0 or height_inches > 120:
                    messagebox.showerror("Invalid height", "Enter height in inches (e.g. 68) between 1 and 120.")
                    return
            except ValueError:
                messagebox.showerror("Invalid height", "Please enter a number (e.g. 68).")
                return

        profile = UserProfile(
            first_name=first,
            last_name=last,
            gender=gender,
            age=age,
            height_inches=height_inches,
        )
        save_user_profile(profile)
        messagebox.showinfo("Saved", "User profile saved.")
        self.dialog.destroy()
