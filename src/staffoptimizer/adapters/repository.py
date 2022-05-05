"""
Repository pattern, a simplifying abstraction over data storage, allow to decouple model layer from data layer.
It hides the boring details of data access by pretending that all data is in memory. Because the objects
are in memory, a .save() method never have to be called; just fetch the object to care about and modify it in memory.

The Repository pattern would make it easy to make fundamental changes to the way things are stored and, it is easy to
fake out for unit tests.

This module is borrowing some artifacts from ports and adapters.
* AbstractRepository is a port : port is the interface between the application and whatever it is we wish to abstract
away
* SQLAlchemyRepository is an adapter: the implementation behind that abstraction
in ports and adapters terminology.

As soon as it's layering in the good way : higher modules don't depend on lower modules, everything's fine.
https://blog.ploeh.dk/2013/12/03/layers-onions-ports-adapters-its-all-the-same/
"""


from src.staffoptimizer.domain import model


class AbstractRepository:
    def add(self, so: model.StaffOptimizer):
        raise NotImplementedError

    def get(self, reference) -> model.StaffOptimizer:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        """
        Session establishes all conversations with the database and represents a “holding zone” for all the objects
        which you’ve loaded or associated with it during its lifespan. It provides the interface where SELECT and other
        queries are made that will return and modify ORM-mapped objects.
        The ORM objects themselves are maintained inside the Session, inside a structure called the identity map -
        a data structure that maintains unique copies of each object, where “unique” means “only one object with a
        particular primary key”.
        https://docs.sqlalchemy.org/en/14/orm/session_basics.html#what-does-the-session-do
        """
        self.session = session

    def add(self, so):
        self.session.add(so)

    def get(self, run_id):
        return self.session.query(model.StaffOptimizer).filter_by(run_id=run_id).one()

    def list(self):
        return self.session.query(model.StaffOptimizer).all()
