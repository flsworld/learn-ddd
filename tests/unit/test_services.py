from src.staffoptimizer.adapters import repository
from src.staffoptimizer.domain import model
from src.staffoptimizer.domain.model import Status
from src.staffoptimizer.service_layer import unit_of_work, services


class FakeSORepository(repository.AbstractRepository):
    def __init__(self, so):
        self._so = set(so)

    def add(self, so):
        self._so.add(so)

    def get(self, run_id):
        return next((so for so in self._so if so.run_id == run_id), None)


class FakeUserRepository(repository.AbstractRepository):
    def __init__(self, user):
        self._user = set(user)

    def add(self, user):
        self._user.add(user)

    def get(self, ref):
        pass

    def get_editor(self, editor_id):
        return next((user for user in self._user if user.editor_id == editor_id), None)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.so = FakeSORepository([])
        self.user = FakeUserRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_assign_returns_taskref():
    uow = FakeUnitOfWork()
    uow.user.add(model.Editor("Medhi", "MB13"))
    services.add_task("Vidéo d'Emma", Status.REVIEW_STAFFING.value, "Arts and Craft", "CR7", uow)
    result = services.assign("MB13", "Vidéo d'Emma", "CR7", uow)
    assert result == "Vidéo d'Emma"
