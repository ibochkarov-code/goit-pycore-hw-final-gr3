"""Tests for handlers/note_handlers.py."""

import pytest

from cli.errors import UsageError
from handlers.note_handlers import (
    handle_add_note,
    handle_add_tags,
    handle_delete_note,
    handle_edit_note,
    handle_remove_tag,
    handle_rename_note,
    handle_search_notes,
    handle_show_all_notes,
)
from models.notebook import NoteBook


@pytest.fixture()
def nb() -> NoteBook:
    nb = NoteBook()
    nb.add_note("Shopping", "Buy milk and eggs")
    nb.add_note("Work", "Finish the report", tags="urgent")
    return nb


class TestAddNote:
    def test_add(self, nb: NoteBook) -> None:
        result = handle_add_note("Ideas", "Learn", "Rust", notebook=nb)
        assert result == "Note 'Ideas' added."
        assert len(nb) == 3
        assert nb.notes[-1].text == "Learn Rust"

    def test_duplicate_title(self, nb: NoteBook) -> None:
        result = handle_add_note("Shopping", "Other text", notebook=nb)
        assert result == "Note 'Shopping' already exists."

    def test_no_args_raises(self) -> None:
        with pytest.raises(UsageError, match="title and text are required"):
            handle_add_note(notebook=NoteBook())

    def test_title_only_raises(self) -> None:
        with pytest.raises(UsageError, match="title and text are required"):
            handle_add_note("Title", notebook=NoteBook())


class TestDeleteNote:
    def test_delete(self, nb: NoteBook) -> None:
        result = handle_delete_note("Shopping", notebook=nb)
        assert result == "Note 'Shopping' deleted."
        assert len(nb) == 1

    def test_not_found(self, nb: NoteBook) -> None:
        result = handle_delete_note("Nonexistent", notebook=nb)
        assert result == "Note 'Nonexistent' not found."

    def test_no_args_raises(self) -> None:
        with pytest.raises(UsageError, match="title is required"):
            handle_delete_note(notebook=NoteBook())


class TestEditNote:
    def test_edit_text(self, nb: NoteBook) -> None:
        result = handle_edit_note("Shopping", "Updated", "text", notebook=nb)
        assert result == "Note 'Shopping' updated."
        assert nb.find_note_by_title("Shopping").text == "Updated text"

    def test_not_found(self, nb: NoteBook) -> None:
        result = handle_edit_note("Nonexistent", "text", notebook=nb)
        assert result == "Note 'Nonexistent' not found."

    def test_preserves_tags(self, nb: NoteBook) -> None:
        handle_edit_note("Work", "New", "text", notebook=nb)
        assert nb.find_note_by_title("Work").tags == ["urgent"]

    def test_not_enough_args_raises(self) -> None:
        with pytest.raises(UsageError, match="title and new text are required"):
            handle_edit_note("Title", notebook=NoteBook())


class TestRenameNote:
    def test_rename(self, nb: NoteBook) -> None:
        result = handle_rename_note("Shopping", "Groceries", notebook=nb)
        assert result == "Note 'Shopping' renamed to 'Groceries'."
        assert nb.find_note_by_title("Groceries") is not None
        assert nb.find_note_by_title("Shopping") is None

    def test_not_found(self, nb: NoteBook) -> None:
        result = handle_rename_note("Nonexistent", "New", notebook=nb)
        assert result == "Note 'Nonexistent' not found."

    def test_target_exists(self, nb: NoteBook) -> None:
        result = handle_rename_note("Shopping", "Work", notebook=nb)
        assert "already exist" in result

    def test_not_enough_args_raises(self) -> None:
        with pytest.raises(UsageError, match="title and new title are required"):
            handle_rename_note("Title", notebook=NoteBook())


class TestAddTags:
    def test_add_tags(self, nb: NoteBook) -> None:
        result = handle_add_tags("Shopping", "food", "weekly", notebook=nb)
        assert result == "Tags added to note 'Shopping'."
        note = nb.find_note_by_title("Shopping")
        assert "food" in note.tags
        assert "weekly" in note.tags

    def test_not_found(self, nb: NoteBook) -> None:
        result = handle_add_tags("Nonexistent", "tag", notebook=nb)
        assert result == "Note 'Nonexistent' not found."

    def test_invalid_tag(self, nb: NoteBook) -> None:
        result = handle_add_tags("Shopping", "bad!tag", notebook=nb)
        assert "Invalid tag" in result

    def test_not_enough_args_raises(self) -> None:
        with pytest.raises(UsageError, match="title and at least one tag"):
            handle_add_tags("Title", notebook=NoteBook())


class TestRemoveTag:
    def test_remove_tag(self, nb: NoteBook) -> None:
        result = handle_remove_tag("Work", "urgent", notebook=nb)
        assert result == "Tag 'urgent' removed from note 'Work'."
        assert nb.find_note_by_title("Work").tags == []

    def test_tag_not_found(self, nb: NoteBook) -> None:
        result = handle_remove_tag("Work", "nonexistent", notebook=nb)
        assert "not found" in result

    def test_note_not_found(self, nb: NoteBook) -> None:
        result = handle_remove_tag("Nonexistent", "tag", notebook=nb)
        assert result == "Note 'Nonexistent' not found."

    def test_not_enough_args_raises(self) -> None:
        with pytest.raises(UsageError, match="title and tag are required"):
            handle_remove_tag("Title", notebook=NoteBook())


class TestSearchNotes:
    def test_found(self, nb: NoteBook) -> None:
        result = handle_search_notes("milk", notebook=nb)
        assert "Shopping" in result

    def test_not_found(self, nb: NoteBook) -> None:
        assert handle_search_notes("xyz", notebook=nb) == "No notes found."

    def test_no_args_raises(self) -> None:
        with pytest.raises(UsageError, match="keyword is required"):
            handle_search_notes(notebook=NoteBook())


class TestShowAllNotes:
    def test_lists_notes(self, nb: NoteBook) -> None:
        result = handle_show_all_notes(notebook=nb)
        assert "Shopping" in result
        assert "Work" in result
        assert "1." in result
        assert "2." in result

    def test_empty_notebook(self) -> None:
        assert handle_show_all_notes(notebook=NoteBook()) == "No notes saved."

    def test_with_args_raises(self, nb: NoteBook) -> None:
        with pytest.raises(UsageError, match="no arguments expected"):
            handle_show_all_notes("x", notebook=nb)
