from healthcheck import HealthCheck
from fastapi import Response, FastAPI
from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
# from core import database
# from models import Message, TopicPartition

# get_db = database.get_db
health = HealthCheck()
router = APIRouter(
    prefix="/checkme",
    tags=['healthcheck']
)


@router.get("/")
def healthcheck():
    message = health.run()
    # status_code, headers = health.run()
    # print(message,status_code,headers)
    # response.status_code = status_code
    # response.headers = headers
    # print(message)
    return message
