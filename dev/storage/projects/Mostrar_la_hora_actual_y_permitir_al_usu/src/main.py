import os
import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

from .config import load_config, save_config
from .clock import Clock
from .notes import Note, load_notes, save_notes, create_note, edit_note, delete_note
from .export import export_notes_to_txt, export_notes_to_pdf


class NotesApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Notes")
        self.geometry("600x400")
        self.config_data = load_config()
        self.notes_file = self.config_data["notes_file"]
        self.notes = load_notes(self.notes_file)

        self.clock = Clock(self)
        self.clock.pack(pady=5)

        self.listbox = tk.Listbox(self, height=15)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self._refresh_listbox()

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add", command=self.add_note).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Edit", command=self.edit_selected).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_selected).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Export TXT", command=self.export_txt).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Export PDF", command=self.export_pdf).grid(row=0, column=4, padx=5)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for note in self.notes:
            display = f"{note.title} ({note.created_at[:10]})"
            self.listbox.insert(tk.END, display)

    def add_note(self):
        title = simpledialog.askstring("New Note", "Title:")
        if title is None:
            return
        content = simpledialog.askstring("New Note", "Content:")
        if content is None:
            return
        note = create_note(title, content)
        self.notes.append(note)
        self._refresh_listbox()

    def _get_selected_note(self) -> Note | None:
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Select Note", "No note selected.")
            return None
        index = selection[0]
        return self.notes[index]

    def edit_selected(self):
        note = self._get_selected_note()
        if not note:
            return
        new_title = simpledialog.askstring("Edit Note", "New Title:", initialvalue=note.title)
        if new_title is None:
            return
        new_content = simpledialog.askstring("Edit Note", "New Content:", initialvalue=note.content)
        if new_content is None:
            return
        edit_note(note, new_title, new_content)
        self._refresh_listbox()

    def delete_selected(self):
        note = self._get_selected_note()
        if not note:
            return
        if messagebox.askyesno("Delete", f"Delete note '{note.title}'?"):
            self.notes = delete_note(self.notes, note.id)
            self._refresh_listbox()

    def export_txt(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if path:
            export_notes_to_txt(self.notes, path)
            messagebox.showinfo("Export", f"Notes exported to {os.path.basename(path)}")

    def export_pdf(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if path:
            export_notes_to_pdf(self.notes, path)
            messagebox.showinfo("Export", f"Notes exported to {os.path.basename(path)}")

    def on_close(self):
        save_notes(self.notes_file, self.notes)
        self.destroy()


if __name__ == "__main__":
    app = NotesApp()
    app.mainloop()
