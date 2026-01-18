import json
import os
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List


@dataclass
class Note:
    id: str
    title: str
    content: str
    created_at: str  # ISO format


def _note_from_dict(data: dict) -> Note:
    return Note(**data)


def load_notes(path: str) -> List[Note]:
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            raw = json.load(f)
        except json.JSONDecodeError:
            raw = []
    return [_note_from_dict(item) for item in raw]


def save_notes(path: str, notes: List[Note]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(note) for note in notes], f, indent=2)


def create_note(title: str, content: str) -> Note:
    return Note(
        id=str(uuid.uuid4()),
        title=title,
        content=content,
        created_at=datetime.utcnow().isoformat()
    )


def edit_note(note: Note, new_title: str, new_content: str) -> Note:
    note.title = new_title
    note.content = new_content
    return note


def delete_note(notes: List[Note], note_id: str) -> List[Note]:
    return [n for n in notes if n.id != note_id]
