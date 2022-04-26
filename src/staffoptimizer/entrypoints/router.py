from fastapi import APIRouter, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.staffoptimizer.service_layer import services, unit_of_work

router = APIRouter()
get_session = sessionmaker(bind=create_engine("sqlite:///:memory:"))


@router.post("/validate", status_code=status.HTTP_200_OK)
def validate_staffing(run_id):
    services.validate(run_id, unit_of_work.SQLAlchemyUnitOfWork())
