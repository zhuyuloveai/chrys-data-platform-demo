from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from chrys_demo import TaskBoard


class TaskBoardTests(unittest.TestCase):
    def test_add_normalizes_title_and_assigns_identifier(self) -> None:
        board = TaskBoard()

        task = board.add("  verify attribution  ")

        self.assertEqual(task.identifier, 1)
        self.assertEqual(task.title, "verify attribution")
        self.assertFalse(task.completed)

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

    def test_unknown_task_cannot_be_completed(self) -> None:
        with self.assertRaises(KeyError):
            TaskBoard().complete(99)


if __name__ == "__main__":
    unittest.main()

