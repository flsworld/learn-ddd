from src.staffoptimizer.adapters import repository
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
    staffed_tasks = [
        ("Midgar", Status.REVIEW_STAFFING.value, "Arts and Craft"),
        ("Chocobo farm", Status.REVIEW_STAFFING.value, "Kosovo"),
    ]
    unallocated_tasks = [
        ("Kalm", Status.REVIEW_STAFFING.value, "Brazil"),
        ("Junon", Status.REVIEW_STAFFING.value, "Arts and Craft"),
    ]

    uow = FakeUnitOfWork()
    run_id = 1
    for task in staffed_tasks + unallocated_tasks:
        services.add_task(*task, run_id, uow)
    # call allocate !!


    services.validate(run_id, uow)

    so = uow.so.get(run_id)
    assert all(t.status == Status.READY_TO_EDIT.value for t in so.staffed_tasks)
    assert all(
        t.status == Status.READY_FOR_STAFFING.value for t in so.unallocated_tasks
    )
    assert uow.committed
