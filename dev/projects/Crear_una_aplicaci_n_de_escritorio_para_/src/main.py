import os
import sys
import tkinter as tk
from tkinter import ttk

# Ensure the directory containing this file is in the module search path
sys.path.append(os.path.dirname(__file__))

from .clock import Clock
from .note_manager import load_note, save_note

class NoteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Reloj y Notas")
        self.geometry("400x300")
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Reloj
        self.clock = Clock(self)
        self.clock.pack(pady=10)

        # Área de notas
        self.text = tk.Text(self, wrap="word")
        self.text.pack(expand=True, fill="both", padx=10, pady=10)
        self.text.insert("1.0", load_note())
        # Reset modified flag after initial load
        self.text.edit_modified(False)

        # Guardar al modificar
        self.text.bind("<<Modified>>", self.on_modified)

    def on_modified(self, event):
        if self.text.edit_modified():
            content = self.text.get("1.0", "end-1c")
            save_note(content)
            self.text.edit_modified(False)

    def on_close(self):
        # Guardar antes de cerrar
        content = self.text.get("1.0", "end-1c")
        save_note(content)
        self.destroy()

if __name__ == "__main__":
    app = NoteApp()
    app.mainloop()
