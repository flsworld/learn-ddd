from src.staffoptimizer.adapters import repository
from src.staffoptimizer.domain.model import Editor, Task, Status, StaffOptimizer
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
    jeff = Editor("Jeff")
    nicole = Editor("Nicole")
    tasks = [
        # Create staffed tasks
        Task("001", "Midgar", Status.REVIEW_STAFFING.value, "Arts and Craft", jeff),
        Task("003", "Chocobo farm", Status.REVIEW_STAFFING.value, "Kosovo", nicole),
        # Create unallocated tasks
        Task("002", "Kalm", Status.REVIEW_STAFFING.value, "Brazil", None),
        Task("004", "Junon", Status.REVIEW_STAFFING.value, "Arts and Craft"),
    ]
    uow = FakeUnitOfWork()
    run_id = services.run_staffoptimizer("F1", tasks, uow)

    services.validate(run_id, uow)

    so = uow.so.get(run_id)
    assert all(t.status == Status.READY_TO_EDIT.value for t in so.staffed_tasks)
    assert all(t.status == Status.REVIEW_STAFFING.value for t in so.unallocated_tasks)
