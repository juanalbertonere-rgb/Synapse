import os
import tempfile
import unittest
from unittest import mock

# Import the module after adjusting the NOTE_FILE path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import note_manager

class TestNoteManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary file to act as the note storage
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.addCleanup(os.unlink, self.temp_file.name)

        # Patch the NOTE_FILE constant in note_manager to point to the temp file
        patcher = mock.patch.object(note_manager, "NOTE_FILE", self.temp_file.name)
        self.mock_note_file = patcher.start()
        self.addCleanup(patcher.stop)

    def test_load_note_file_not_exists(self):
        # Ensure the temp file is removed to simulate missing file
        os.unlink(self.temp_file.name)
        content = note_manager.load_note()
        self.assertEqual(content, "")

    def test_save_and_load_note(self):
        test_content = "Esta es una nota de prueba."
        note_manager.save_note(test_content)

        # Verify file content directly
        with open(self.temp_file.name, "r", encoding="utf-8") as f:
            file_content = f.read()
        self.assertEqual(file_content, test_content)

        # Verify load_note returns the same content
        loaded = note_manager.load_note()
        self.assertEqual(loaded, test_content)

if __name__ == "__main__":
    unittest.main()
