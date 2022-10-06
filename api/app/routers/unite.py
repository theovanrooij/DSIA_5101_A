from fastapi import APIRouter, Depends
# from services import students as students_service
import schemas, models
from sqlalchemy.orm import Session

router = APIRouter(prefix="/unites")
