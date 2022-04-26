import abc
from src.staffoptimizer.domain import model


class AbstractRepository(abc.ABC):
    """
    Aka the port, in ports and adapters terminology
    """
    @abc.abstractmethod
    def add(self, so: model.StaffOptimizer):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.StaffOptimizer:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, so):
        self.session.add(so)

    def get(self, run_id):
        return self.session.query(model.StaffOptimizer).filter_by(run_id=run_id).one()

    def list(self):
        return self.session.query(model.StaffOptimizer).all()
