import tkinter as tk
from datetime import datetime
from .config import load_config


class Clock(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.time_label = tk.Label(self, font=("Helvetica", 16))
        self.time_label.pack()
        self.time_format = load_config().get("time_format", "%H:%M:%S")
        self._update_clock()

    def _update_clock(self):
        now = datetime.now().strftime(self.time_format)
        self.time_label.config(text=now)
        self.after(1000, self._update_clock)
