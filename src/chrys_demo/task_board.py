"""A deliberately small domain model for end-to-end coding experiments."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum


class Priority(StrEnum):
    """Task urgency, ordered from most to least important."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


_PRIORITY_RANK = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}


def _normalize_tags(tags: Iterable[str]) -> frozenset[str]:
    normalized = {tag.strip().lower() for tag in tags}
    normalized.discard("")
    return frozenset(normalized)


@dataclass(frozen=True)
class Task:
    """One task tracked by the board."""

    identifier: int
    title: str
    completed: bool = False
    priority: Priority = Priority.MEDIUM
    tags: frozenset[str] = frozenset()


class TaskBoard:
    """An in-memory task board with deterministic identifiers."""

    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def add(
        self,
        title: str,
        priority: Priority = Priority.MEDIUM,
        tags: Iterable[str] = (),
    ) -> Task:
        normalized = title.strip()
        if not normalized:
            raise ValueError("task title must not be empty")
        task = Task(
            identifier=len(self._tasks) + 1,
            title=normalized,
            priority=Priority(priority),
            tags=_normalize_tags(tags),
        )
        self._tasks.append(task)
        return task

    def complete(self, identifier: int) -> Task:
        for index, task in enumerate(self._tasks):
            if task.identifier == identifier:
                completed = Task(
                    identifier=task.identifier,
                    title=task.title,
                    completed=True,
                    priority=task.priority,
                    tags=task.tags,
                )
                self._tasks[index] = completed
                return completed
        raise KeyError(identifier)

    def reopen(self, identifier: int) -> Task:
        for index, task in enumerate(self._tasks):
            if task.identifier == identifier:
                if not task.completed:
                    return task
                reopened = Task(
                    identifier=task.identifier,
                    title=task.title,
                    completed=False,
                    priority=task.priority,
                    tags=task.tags,
                )
                self._tasks[index] = reopened
                return reopened
        raise KeyError(identifier)

    def all(self) -> tuple[Task, ...]:
        return tuple(self._tasks)

    def pending(self) -> tuple[Task, ...]:
        pending_tasks = [task for task in self._tasks if not task.completed]
        pending_tasks.sort(key=lambda task: _PRIORITY_RANK[task.priority])
        return tuple(pending_tasks)

    def by_tag(self, tag: str) -> tuple[Task, ...]:
        target = tag.strip().lower()
        return tuple(task for task in self._tasks if target in task.tags)
