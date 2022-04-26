from fastapi import FastAPI

from src.staffoptimizer.adapters import orm
from src.staffoptimizer.entrypoints.router import router

orm.start_mappers()
app = FastAPI()

app.include_router(router)

