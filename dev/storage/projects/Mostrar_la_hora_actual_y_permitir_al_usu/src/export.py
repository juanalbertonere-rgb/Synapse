import os
from typing import List

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

from .notes import Note


def export_notes_to_txt(notes: List[Note], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for note in notes:
            f.write(f"Title: {note.title}\n")
            f.write(f"Created: {note.created_at}\n")
            f.write(f"{note.content}\n")
            f.write("-" * 40 + "\n")


def export_notes_to_pdf(notes: List[Note], path: str) -> None:
    c = canvas.Canvas(path, pagesize=LETTER)
    width, height = LETTER
    y = height - 50
    for note in notes:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Title: {note.title}")
        y -= 15
        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Created: {note.created_at}")
        y -= 15
        text_obj = c.beginText(50, y)
        text_obj.textLines(note.content)
        c.drawText(text_obj)
        y = text_obj.getY() - 20
        if y < 100:
            c.showPage()
            y = height - 50
    c.save()
