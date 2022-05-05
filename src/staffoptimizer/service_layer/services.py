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


from src.staffoptimizer.domain.model import Status, StaffOptimizer

from . import unit_of_work


class HungerStrike(Exception):
    pass


def run_staffoptimizer(run_id, uow):
    """
    Schematization of a job run. Allocating tasks doesn't come from nowhere.
    """
    with uow:
        so = uow.so.get(run_id)
        if so is None:
            so = StaffOptimizer(run_id, so.tasks)
            uow.so.add(so)
        uow.commit()
    return run_id


def validate(run_id: int, uow: unit_of_work.AbstractUnitOfWork):
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
