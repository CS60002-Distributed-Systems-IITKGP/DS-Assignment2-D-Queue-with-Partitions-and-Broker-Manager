import health
import consumer
import producer
import topics
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
# from core.config import settings
from core.database import engine
from core import base, database
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from models import Broker

get_db = database.get_db

# add routers
#import producer
#import consumer
# import size

# all models -> db tables
base.Base.metadata.create_all(engine)


app = FastAPI(title="Broker-Manager")


app.add_middleware(
    CORSMiddleware,
    # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_origins=["http://localhost:8000", "https://localhost:8000",
                   "http://localhost", "https://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# db
get_db = database.get_db


app.include_router(topics.router)
# app.include_router(producer.router)
# app.include_router(consumer.router)
app.include_router(producer.router)
app.include_router(consumer.router)
app.include_router(health.router)
# app.include_router(size.router)


@app.get('/')
def index():
    return {"hello": "broker-manager"}


class BrokerData(BaseModel):
    broker_address: str
    hostname: Optional[str] = None


class InitDataRequest(BaseModel):
    broker_data: List[BrokerData] = []


@app.post("/init-brokers-data")
def init_broker_data(request: InitDataRequest, db: Session = Depends(get_db)):
    for data in request.broker_data:
        # create broker db row
        broker = Broker(address=data.broker_address, hostname=data.hostname)
        db.add(broker)

    db.commit()
    # get all brokers data
    brokers = db.query(Broker).all()

    return {
        "message": "brokers data added successfully",
        "brokers": brokers
    }
