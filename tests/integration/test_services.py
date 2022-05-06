from src.staffoptimizer.adapters import repository
from src.staffoptimizer.domain import model
from src.staffoptimizer.domain.model import Status
from src.staffoptimizer.service_layer import unit_of_work, services


class FakeRepository(repository.AbstractRepository):
    def __init__(self, so):
        self._so = set(so)

    def add(self, so):
        self._so.add(so)

    def get(self, run_id):
        return next((so for so in self._so if so.run_id == run_id), None)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.so = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_validate_after_so_run():
    allocations = [
        (("Midgar", Status.REVIEW_STAFFING.value, "Arts and Craft"), "MB13"),
        (("Chocobo farm", Status.REVIEW_STAFFING.value, "Kosovo"), "FLS92"),
    ]

    uow = FakeUnitOfWork()
    run_id = "KB9"
    for task, editor_id in allocations:
        ref, status, team = task
        services.add_task(ref, status, team, run_id, uow)
        services.assign(editor_id, ref, run_id, uow)

    services.validate(run_id, uow)

    so = uow.so.get(run_id)
    assert all(t.status == Status.READY_TO_EDIT.value for t in so.staffed_tasks)
    assert all(
        t.status == Status.READY_FOR_STAFFING.value for t in so.unallocated_tasks
    )
    assert uow.committed
