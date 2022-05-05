"""
The most important thing an ORM gives us is persistence ignorance: the idea that our fancy domain model doesn’t
need to know anything about how data is loaded or persisted. This helps keep the domain clean of direct
dependencies on particular database technologies.

Here, the usual way, defined in the SQLAlchemy tutorial, for associating model classes to a declarative_base() function
has not been used. Because the target architecture is clearly to apply the DIP : avoid model properties to depend on
storage concerns.
https://docs.sqlalchemy.org/en/14/orm/tutorial.html#declare-a-mapping

Instead, a mapper is used to make the model aware of the infrastructure layer only when start_mappers() is invoked.
https://docs.sqlalchemy.org/en/14/orm/mapping_api.html?#sqlalchemy.orm.mapper 
"""


from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.orm import mapper

from src.staffoptimizer.domain import model

metadata = MetaData()

tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255)),
)
user = Table()


def start_mappers():
    tasks_mapper = mapper(model.Task, tasks)
