"""
This module is a placeholder in which will be stored all entities that serve to model business processes.
A model is a map of a process or phenomenon that captures a useful property.
The domain model is the mental map that business owners have of their businesses. All business people have these mental
map - they’re how humans think about complex processes.

DDD says that the most important thing about software is that it provides a useful model of a problem.
If we get that model right, our software delivers value and makes new things possible.

DDD book:
* The original "blue book", Domain-Driven Design by Eric Evans
* The "red book", Implementing Domain-Driven Design by Vaughn Vernon

This is the part of the code that is closest to the business, the most likely to change, and the place where the most
value to the business is delivered. This should be easy to understand and modify

In here we'll also put domain service. It is a piece of logic that belongs in the domain model but doesn’t sit
naturally inside a stateful model class. Instead, a stateless class or function can do the job.
"""


from enum import Enum
from typing import Optional


class Status(Enum):
    READY_FOR_STAFFING = 1
    REVIEW_STAFFING = 2
    READY_TO_EDIT = 3


class User:
    def __init__(self, name):
        self.name = name


class Editor(User):
    pass


class Task:
    def __init__(
        self,
        ref,
        title,
        status,
        team,
        editor: Optional[Editor] = None,
        run_id: Optional[int] = None,
    ):
        self.reference = ref
        self.title = title
        self.status = status
        self.editor = editor
        self.team = team
        self.run_id = run_id

    @property
    def staffed(self):
        return self.status > Status.READY_FOR_STAFFING.value and self.editor

    @property
    def unallocated(self):
        return self.status > Status.READY_FOR_STAFFING.value and self.editor is None

    @property
    def computed_by_so(self):
        return self.run_id is not None


class StaffOptimizer:
    def __init__(self, run_id, tasks):
        self.run_id = run_id
        self.tasks = tasks

    @property
    def staffed_tasks(self):
        return [task for task in self.tasks if task.staffed]

    @property
    def unallocated_tasks(self):
        return [task for task in self.tasks if task.unallocated]
