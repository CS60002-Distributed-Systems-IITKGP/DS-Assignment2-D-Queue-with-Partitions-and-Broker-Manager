from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from core import database
from models import Producer, Consumer, Topic, ConsumerPartition, Partition, BrokerStatusEnum, Broker
from pydantic import BaseModel
import requests
import aiohttp
import asyncio
import json

get_db = database.get_db

router = APIRouter(
    prefix="/health",
    tags=['health']
)


async def fetch(session: aiohttp.ClientSession, url):
    async with session.get(url) as response:
        return await response.json()


@router.get('/')
async def health(db: Session = Depends(get_db),):
    brokers = db.query(Broker).all()
    # print(brokers, len(brokers))
    if len(brokers) == 0:
        raise HTTPException(status_code=404, detail="No brokers available")
    # for broker in brokers:
        # print(broker.broker_id, broker.address, broker.hostname)
    response = []
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = []
        for broker in brokers:
            task = asyncio.ensure_future(
                fetch(session, url=f'{broker.address}/checkme/'))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        # print(responses)
        for i in range(len(responses)):
            response_body = json.loads(responses[i][0])
            status = response_body['status']
            ts = response_body['timestamp']
            # print(status, ts)
            response.append({
                "broker": brokers[i].broker_id,
                "status": status,
                "timestamp": ts
            })
            brokers[i].active = BrokerStatusEnum.ACTIVE if status == 'success' else BrokerStatusEnum.FAILED
        # brokers[i].last_timestamp = ts

        # for broker in brokers:
        #     broker = db.query(Broker).filter(Broker.broker_id == broker.broker_id)
        #     broker.update(broker)
        #     print(broker)
        db.commit()
        brokers1 = db.query(Broker).all()
        for broker in brokers1:
            print(broker)
        # db.refresh()
    # topic_list = []
    # for topic in topics:
    #     topic_list.append(topic.topic_name)
    return response

# brokers = db.query(Broker).all()
