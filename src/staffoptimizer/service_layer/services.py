"""
Here stands the service layer, which serve as the entrypoint to the domain model. An abstraction to capture the use
case and that will sit between FastAPI and the domain model. Its job is to handle requests from the outside world and
to orchestrate an operation. This is separated from business logic and helps keeping things tidy.

Orchestration layer or a use-case layer :
* fetching stuff out of the repository
* validating the input against database state
* handling errors
* update the domain model
* committing in the happy path - persisting any changes
Things that could be related to an API, CLI or tests !

Using primitive data types allows the service layer’s clients (tests and FastAPI) to be decoupled from the model
layer. If the domain model is refactored, this will have no impact on the orchestration layer.
"""
from typing import Optional

from src.staffoptimizer.domain.model import Status, StaffOptimizer

from . import unit_of_work
from ..domain import model


class HungerStrike(Exception):
    pass


class SORunNotFound(Exception):
    pass


class TaskNotFound(Exception):
    pass


def add_task(
    title: str,
    status: str,
    team: str,
    run_id: Optional[str],
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        so = uow.so.get(run_id)
        if so is None:
            so = StaffOptimizer(run_id, tasks=[])
            uow.so.add(so)
        so.tasks.append(model.Task(title, status, team))
        uow.commit()
    return run_id


def add_editor(name: str, editor_id: str, uow: unit_of_work.AbstractUnitOfWork):
    pass


def assign(
    editor_id: str,
    ref: str,
    run_id: str,
    uow: unit_of_work.AbstractUnitOfWork,
) -> str:
    with uow:
        so = uow.so.get(run_id)
        if so is None:
            raise SORunNotFound(f"Invalid run_id {run_id}")
        task = next((t for t in so.tasks if t.reference == ref), None)
        if task is None:
            raise TaskNotFound(f"Invalid reference {ref}")
        editor = next(
            (e for t in so.tasks for e in t._assignments if e.editor_id == editor_id),
            None,
        )
        # TODO: handle typing
        taskref = so.assign(editor, task)
        uow.commit()
    return taskref


def validate(run_id: str, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        so = uow.so.get(run_id)
        if not so.tasks:
            raise HungerStrike("Not a single task to run in the StaffOptimizer")

        # To meditate : should we call a domain service instead ?
        # task.update_status() ?
        for task in so.staffed_tasks:
            task.status = Status.READY_TO_EDIT.value

        for task in so.unallocated_tasks:
            task.status = Status.READY_FOR_STAFFING.value

        uow.commit()

    return so.run_id
