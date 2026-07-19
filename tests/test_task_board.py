from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from chrys_demo import Priority, TaskBoard


class TaskBoardTests(unittest.TestCase):
    def test_add_normalizes_title_and_assigns_identifier(self) -> None:
        board = TaskBoard()

        task = board.add("  verify attribution  ")

        self.assertEqual(task.identifier, 1)
        self.assertEqual(task.title, "verify attribution")
        self.assertFalse(task.completed)
        self.assertEqual(task.priority, Priority.MEDIUM)

    def test_add_accepts_priority(self) -> None:
        board = TaskBoard()

        task = board.add("capture session", Priority.HIGH)

        self.assertEqual(task.priority, Priority.HIGH)

    def test_add_accepts_priority_as_string(self) -> None:
        board = TaskBoard()

        task = board.add("capture session", "low")

        self.assertEqual(task.priority, Priority.LOW)

    def test_add_rejects_unknown_priority(self) -> None:
        with self.assertRaises(ValueError):
            TaskBoard().add("capture session", "urgent")

    def test_default_task_priority_is_medium(self) -> None:
        self.assertEqual(TaskBoard().add("x").priority, Priority.MEDIUM)

    def test_empty_title_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            TaskBoard().add("   ")

    def test_complete_updates_pending_tasks(self) -> None:
        board = TaskBoard()
        first = board.add("capture session")
        second = board.add("upload attribution")

        completed = board.complete(first.identifier)

        self.assertTrue(completed.completed)
        self.assertEqual(board.pending(), (second,))

    def test_complete_preserves_priority(self) -> None:
        board = TaskBoard()
        task = board.add("capture session", Priority.HIGH)

        completed = board.complete(task.identifier)

        self.assertEqual(completed.priority, Priority.HIGH)

    def test_unknown_task_cannot_be_completed(self) -> None:
        with self.assertRaises(KeyError):
            TaskBoard().complete(99)

    def test_reopen_marks_task_as_pending_again(self) -> None:
        board = TaskBoard()
        first = board.add("capture session")
        second = board.add("upload attribution")
        board.complete(first.identifier)

        reopened = board.reopen(first.identifier)

        self.assertFalse(reopened.completed)
        self.assertEqual(set(board.pending()), {first, second})

    def test_reopen_preserves_priority(self) -> None:
        board = TaskBoard()
        task = board.add("capture session", Priority.HIGH)
        board.complete(task.identifier)

        reopened = board.reopen(task.identifier)

        self.assertEqual(reopened.priority, Priority.HIGH)

    def test_reopen_preserves_tags(self) -> None:
        board = TaskBoard()
        task = board.add("capture session", tags=["python", "demo"])
        board.complete(task.identifier)

        reopened = board.reopen(task.identifier)

        self.assertEqual(reopened.tags, frozenset({"python", "demo"}))

    def test_reopen_is_idempotent_on_pending_task(self) -> None:
        board = TaskBoard()
        task = board.add("capture session")

        first = board.reopen(task.identifier)
        second = board.reopen(task.identifier)

        self.assertIs(first, second)
        self.assertFalse(second.completed)

    def test_unknown_task_cannot_be_reopened(self) -> None:
        with self.assertRaises(KeyError):
            TaskBoard().reopen(99)

    def test_pending_orders_by_priority(self) -> None:
        board = TaskBoard()
        low = board.add("low task", Priority.LOW)
        high = board.add("high task", Priority.HIGH)
        medium = board.add("medium task", Priority.MEDIUM)

        self.assertEqual(board.pending(), (high, medium, low))

    def test_pending_is_stable_within_same_priority(self) -> None:
        board = TaskBoard()
        first_high = board.add("first high", Priority.HIGH)
        second_high = board.add("second high", Priority.HIGH)
        low = board.add("low task", Priority.LOW)

        self.assertEqual(board.pending(), (first_high, second_high, low))

    def test_pending_excludes_completed_tasks_after_sorting(self) -> None:
        board = TaskBoard()
        low = board.add("low task", Priority.LOW)
        high = board.add("high task", Priority.HIGH)
        board.complete(high.identifier)

        self.assertEqual(board.pending(), (low,))

    def test_default_task_has_no_tags(self) -> None:
        task = TaskBoard().add("untagged task")

        self.assertEqual(task.tags, frozenset())

    def test_add_accepts_tags(self) -> None:
        task = TaskBoard().add("capture session", tags=["python", "demo"])

        self.assertEqual(task.tags, frozenset({"python", "demo"}))

    def test_add_normalizes_and_deduplicates_tags(self) -> None:
        task = TaskBoard().add(
            "capture session",
            tags=["  Python ", "python", "DEMO", "", "  "],
        )

        self.assertEqual(task.tags, frozenset({"python", "demo"}))

    def test_add_tags_are_immutable(self) -> None:
        task = TaskBoard().add("capture session", tags=["python"])

        self.assertIsInstance(task.tags, frozenset)

    def test_complete_preserves_tags(self) -> None:
        board = TaskBoard()
        task = board.add("capture session", tags=["python", "demo"])

        completed = board.complete(task.identifier)

        self.assertEqual(completed.tags, frozenset({"python", "demo"}))

    def test_by_tag_matches_tasks(self) -> None:
        board = TaskBoard()
        python_demo = board.add("capture session", tags=["python", "demo"])
        python_only = board.add("upload attribution", tags=["python"])
        rust = board.add("ingest events", tags=["rust"])

        self.assertEqual(board.by_tag("python"), (python_demo, python_only))

    def test_by_tag_is_case_insensitive_and_trims_input(self) -> None:
        board = TaskBoard()
        task = board.add("capture session", tags=["python"])

        self.assertEqual(board.by_tag("  PYTHON  "), (task,))

    def test_by_tag_includes_completed_tasks(self) -> None:
        board = TaskBoard()
        task = board.add("capture session", tags=["python"])
        board.complete(task.identifier)

        matched = board.by_tag("python")

        self.assertEqual(len(matched), 1)
        self.assertTrue(matched[0].completed)

    def test_by_tag_with_unknown_tag_returns_empty(self) -> None:
        board = TaskBoard()
        board.add("capture session", tags=["python"])

        self.assertEqual(board.by_tag("rust"), ())

    def test_by_tag_with_empty_query_returns_empty(self) -> None:
        board = TaskBoard()
        board.add("capture session", tags=["python"])

        self.assertEqual(board.by_tag("   "), ())


if __name__ == "__main__":
    unittest.main()
