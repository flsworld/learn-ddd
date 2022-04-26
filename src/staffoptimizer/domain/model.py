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
