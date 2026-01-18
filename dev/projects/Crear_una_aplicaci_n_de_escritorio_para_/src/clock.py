import tkinter as tk
import time

class Clock(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(font=("Helvetica", 24))
        self.update_time()

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.config(text=current_time)
        self.after(1000, self.update_time)
