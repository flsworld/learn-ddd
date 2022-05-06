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
    # The kind of relationship with other user entities is an "is-a". That's the reason why
    # inheritance will be preferred over composition ("has-a")
    # TODO: Does the User table need to contain all attributes from all inherited classes ?
    # Maybe the User table shouldn't be persisted..?
    # Maybe we could do something like Django
    # https://docs.djangoproject.com/en/4.0/topics/db/models/#model-inheritance-1
    def __init__(self, name: str):
        self.name = name


class ContentStrategist(User):
    def __init__(self, name: str, csid: str):
        super().__init__(name)
        self.csid = csid


class EditorSupervisor(User):
    def __init__(self, name: str, esid: str):
        super().__init__(name)
        self.esid = esid


class Editor(User):
    def __init__(self, name: str, editor_id: str):
        super().__init__(name)
        # Next step here : implement Value Object & Entity pattern
        # This will help to better identify model objects.
        # A good approach when dealing with Entities is to get an identifier close to the real identification of the
        # object in the domain. For instance : registration_number (matricule)
        self.editor_id = editor_id


class Task:
    def __init__(
        self,
        ref: str,  # title is the reference ATM
        status: str,
        team: str,
        run_id: Optional[str] = None,
    ):
        self.reference = ref
        self.status = status
        self.team = team
        self.run_id = run_id
        self._assignments = set()  # type: set[User]

    def assign(self, user: User):
        self._assignments.add(user)

    def unassign(self, user: User):
        if user in self._assignments:
            self._assignments.remove(user)

    @property
    def staffed(self):
        return self.status > Status.READY_FOR_STAFFING.value and any(
            isinstance(user, Editor) for user in self._assignments
        )

    @property
    def unallocated(self):
        """
        "Unallocated" here represents the fact that the task isn't handled by an editor.
        This term is used in a well-defined and bounded context. It is common jargon used
        by the project's team (dev, qa, po, ...) and the domain experts.
        This ubiquitous language between all actors of the projects is very important !
        Dedicated meeting where all these actors sit around the same table to discuss about
        it is crucial !
        """
        return self.status > Status.READY_FOR_STAFFING.value and not any(
            isinstance(user, Editor) for user in self._assignments
        )

    @property
    def computed_by_so(self):
        return self.run_id is not None


class StaffOptimizer:
    def __init__(self, run_id: str, tasks: list[Task]):
        self.run_id = run_id
        self.tasks = tasks

    def assign(self, editor: Editor, task: Task):
        task.assign(editor)
        return task.reference

    @property
    def staffed_tasks(self):
        return [task for task in self.tasks if task.staffed]

    @property
    def unallocated_tasks(self):
        return [task for task in self.tasks if task.unallocated]
