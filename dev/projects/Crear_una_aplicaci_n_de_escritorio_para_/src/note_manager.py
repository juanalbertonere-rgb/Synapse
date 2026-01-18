import os

NOTE_FILE = os.path.join(os.path.dirname(__file__), "note.txt")

def load_note() -> str:
    """Carga el contenido de la nota desde el archivo local."""
    try:
        with open(NOTE_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""
    except Exception:
        return ""

def save_note(content: str) -> None:
    """Guarda el contenido de la nota en el archivo local."""
    try:
        with open(NOTE_FILE, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception:
        pass
