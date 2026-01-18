import os
import json
import tempfile

import pytest

from src.notes import (
    Note,
    create_note,
    edit_note,
    delete_note,
    load_notes,
    save_notes,
)


@pytest.fixture
def temp_file():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_create_note():
    note = create_note("Test", "Content")
    assert isinstance(note, Note)
    assert note.title == "Test"
    assert note.content == "Content"
    assert note.id is not None
    assert note.created_at is not None


def test_edit_note():
    note = create_note("Old", "Old content")
    edited = edit_note(note, "New", "New content")
    assert edited.title == "New"
    assert edited.content == "New content"


def test_delete_note():
    n1 = create_note("One", "1")
    n2 = create_note("Two", "2")
    notes = [n1, n2]
    notes = delete_note(notes, n1.id)
    assert len(notes) == 1
    assert notes[0].id == n2.id


def test_save_and_load_notes(temp_file):
    notes = [create_note("A", "Alpha"), create_note("B", "Beta")]
    save_notes(temp_file, notes)

    # Verify file content is valid JSON
    with open(temp_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, list)
    assert len(data) == 2

    loaded = load_notes(temp_file)
    assert len(loaded) == 2
    titles = {n.title for n in loaded}
    assert titles == {"A", "B"}


def test_load_nonexistent_returns_empty():
    non_path = "nonexistent_file.json"
    notes = load_notes(non_path)
    assert notes == []
