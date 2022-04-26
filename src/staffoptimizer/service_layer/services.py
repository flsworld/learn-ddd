from src.staffoptimizer.domain.model import Status, StaffOptimizer

from . import unit_of_work


def run_staffoptimizer(run_id, tasks, uow):
    with uow:
        so = uow.so.get(run_id)
        if so is None:
            so = StaffOptimizer(run_id, tasks)
            uow.so.add(so)
        uow.commit()
    return run_id


def validate(run_id: int, uow: unit_of_work.AbstractUnitOfWork):
    with uow:
        so = uow.so.get(run_id)
        if not so.tasks:
            return

        for task in so.staffed_tasks:
            task.status = Status.READY_TO_EDIT.value

        for task in so.unallocated_tasks:
            task.status = Status.REVIEW_STAFFING.value

        uow.commit()

    return so.run_id
