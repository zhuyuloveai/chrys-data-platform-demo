"""A deliberately small domain model for end-to-end coding experiments."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Task:
    """One task tracked by the board."""

    identifier: int
    title: str
    completed: bool = False


class TaskBoard:
    """An in-memory task board with deterministic identifiers."""

    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def add(self, title: str) -> Task:
        normalized = title.strip()
        if not normalized:
            raise ValueError("task title must not be empty")
        task = Task(identifier=len(self._tasks) + 1, title=normalized)
        self._tasks.append(task)
        return task

    def complete(self, identifier: int) -> Task:
        for index, task in enumerate(self._tasks):
            if task.identifier == identifier:
                completed = Task(
                    identifier=task.identifier,
                    title=task.title,
                    completed=True,
                )
                self._tasks[index] = completed
                return completed
        raise KeyError(identifier)

    def all(self) -> tuple[Task, ...]:
        return tuple(self._tasks)

    def pending(self) -> tuple[Task, ...]:
        return tuple(task for task in self._tasks if not task.completed)

