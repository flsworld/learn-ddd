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


from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, relationship

from src.staffoptimizer.domain import model

metadata = MetaData()

staffoptimizers = Table(
    "staffoptimizers",
    metadata,
    Column("run_id", String(255)),
)
tasks = Table(
    "tasks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("run_id", ForeignKey("staffoptimizer_runs.id")),
    Column("reference", String(255)),
    Column("status", String(255)),
    Column("team", String(255)),
)
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("editor_id", String(255)),
    Column("csid", String(255)),
    Column("esid", String(255)),
)
assignments = Table(
    "assignments",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("task_id", ForeignKey("tasks.id")),
    Column("user_id", ForeignKey("users.id")),
)


def start_mappers():
    users_mapper = mapper(model.User, users)
    tasks_mapper = mapper(
        model.Task,
        tasks,
        properties={
            "_assignments": relationship(
                users_mapper,
                secondary=assignments,
                collection_class=set,
            )
        },
    )
    mapper(
        model.StaffOptimizer,
        staffoptimizers,
        properties={"tasks": relationship(tasks_mapper)},
    )
