"""
Unit of Work (UoW) pattern is an abstraction over the idea of atomic operations, an abstraction around data integrity.
It allows to finally and fully decouple the service layer from the data layer. It helps to enforce the consistency of
the domain model, and improves performance, by offering to perform a single flush operation at the end of an operation.

With UoW managing database state, FastAPI now does only two things: it initializes a unit of work, and it invokes a
service. The service collaborates with the UoW (think of the UoW as part of the service layer), but neither the service
function itself nor FastAPI now needs to talk directly to the database.

The Unit of Work pattern completes the abstractions over data access by representing atomic updates. Each of the
service-layer use cases runs in a single unit of work that succeeds or fails as a block.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.staffoptimizer.adapters import repository


class AbstractUnitOfWork:
    so: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError


DEFAULT_SESSION_FACTORY = sessionmaker(bind=create_engine("sqlite:///:memory:"))


class SQLAlchemyUnitOfWork(AbstractUnitOfWork):
    """
    A simpler abstraction over the SQLAlchemy Session object has been introduced in order to "narrow" the interface
    between the ORM and our code. This helps to keep us loosely coupled.
    """
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.so = repository.SQLAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

