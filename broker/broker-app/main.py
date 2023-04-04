from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from core.config import settings
from core.database import engine
from core import base, database

# # add routers
import partition

import healthcheckbroker
# import producer
# import consumer
import producer
import consumer
# import size
# import topics


# all models -> db tables
base.Base.metadata.create_all(engine)


app = FastAPI(title="Broker")


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

app.include_router(partition.router)
app.include_router(healthcheckbroker.router)
# app.include_router(topics.router)
app.include_router(producer.router)
app.include_router(consumer.router)
# app.include_router(size.router)


@app.get('/')
def index():
    return {"hello": "broker"}
