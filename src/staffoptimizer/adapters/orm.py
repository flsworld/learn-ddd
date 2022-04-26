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


def start_mappers():
    tasks_mapper = mapper(model.Task, tasks)
