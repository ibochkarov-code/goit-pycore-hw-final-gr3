import pytest

from models.note import Note
from models.notebook import NoteBook


class TestNote:
    def test_create_with_text(self) -> None:
        note = Note("hello")
        assert note.text == "hello"
        assert note.tags == []

    def test_create_with_tags(self) -> None:
        note = Note("hello", tags=["work", "urgent"])
        assert note.tags == ["work", "urgent"]

    def test_matches_text(self) -> None:
        note = Note("Buy groceries")
        assert note.matches("groceries") is True

    def test_matches_text_case_insensitive(self) -> None:
        note = Note("Buy groceries")
        assert note.matches("GROCERIES") is True

    def test_matches_tag(self) -> None:
        note = Note("hello", tags=["work"])
        assert note.matches("work") is True

    def test_matches_tag_case_insensitive(self) -> None:
        note = Note("hello", tags=["Work"])
        assert note.matches("WORK") is True

    def test_no_match(self) -> None:
        note = Note("hello", tags=["work"])
        assert note.matches("xyz") is False

    def test_repr(self) -> None:
        note = Note("hello", tags=["a"])
        result = repr(note)
        assert "hello" in result
        assert "a" in result


class TestNoteBook:
    @pytest.fixture()
    def nb(self) -> NoteBook:
        nb = NoteBook()
        nb.add_note("First note", tags=["work"])
        nb.add_note("Second note", tags=["personal"])
        return nb

    def test_add_note(self) -> None:
        nb = NoteBook()
        nb.add_note("hello")
        assert len(nb) == 1

    def test_add_note_with_tags(self) -> None:
        nb = NoteBook()
        nb.add_note("hello", tags=["a", "b"])
        assert nb.notes[0].tags == ["a", "b"]

    def test_len(self, nb: NoteBook) -> None:
        assert len(nb) == 2

    def test_delete_note_valid(self, nb: NoteBook) -> None:
        assert nb.delete_note(0) is True
        assert len(nb) == 1
        assert nb.notes[0].text == "Second note"

    def test_delete_note_invalid_index(self, nb: NoteBook) -> None:
        assert nb.delete_note(5) is False
        assert len(nb) == 2

    def test_delete_note_negative_index(self, nb: NoteBook) -> None:
        assert nb.delete_note(-1) is False

    def test_edit_note_text(self, nb: NoteBook) -> None:
        assert nb.edit_note(0, new_text="Updated") is True
        assert nb.notes[0].text == "Updated"

    def test_edit_note_tags(self, nb: NoteBook) -> None:
        assert nb.edit_note(0, new_tags=["new_tag"]) is True
        assert nb.notes[0].tags == ["new_tag"]

    def test_edit_note_both(self, nb: NoteBook) -> None:
        assert nb.edit_note(0, new_text="New", new_tags=["t"]) is True
        assert nb.notes[0].text == "New"
        assert nb.notes[0].tags == ["t"]

    def test_edit_note_preserves_unchanged(self, nb: NoteBook) -> None:
        original_tags = nb.notes[0].tags.copy()
        nb.edit_note(0, new_text="Changed text only")
        assert nb.notes[0].tags == original_tags

    def test_edit_note_invalid_index(self, nb: NoteBook) -> None:
        assert nb.edit_note(5, new_text="x") is False

    def test_search_by_text(self, nb: NoteBook) -> None:
        results = nb.search("First")
        assert len(results) == 1
        assert results[0].text == "First note"

    def test_search_by_tag(self, nb: NoteBook) -> None:
        results = nb.search("personal")
        assert len(results) == 1
        assert results[0].text == "Second note"

    def test_search_no_match(self, nb: NoteBook) -> None:
        assert nb.search("xyz") == []

    def test_search_common_word(self, nb: NoteBook) -> None:
        results = nb.search("note")
        assert len(results) == 2

    def test_empty_notebook(self) -> None:
        nb = NoteBook()
        assert len(nb) == 0
        assert nb.search("anything") == []
