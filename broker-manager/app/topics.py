from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from core import database
from models import Producer, Consumer, Topic, ConsumerPartition, Partition, BrokerStatusEnum, Broker
from pydantic import BaseModel
import requests
import httpx
import aiohttp
import asyncio
from core.base import httpx_client

get_db = database.get_db

# client = http3.AsyncClient()

router = APIRouter(
    prefix="/topics",
    tags=['topics']
)


async def fetch(session: aiohttp.ClientSession, url, data):
    async with session.post(url, json=data) as response:
        return await response.json()


class TopicRequest(BaseModel):
    topic_name: str


@router.get('/')
def all(db: Session = Depends(get_db),):
    topics = db.query(Topic).filter(
        # Topic.topic_name == ''
    ).all()
    if len(topics) == 0:
        raise HTTPException(status_code=404, detail="No topics found")
    topic_list = []
    for topic in topics:
        topic_list.append(topic.topic_name)
    return {"topics": topic_list}


@router.post('/', status_code=status.HTTP_201_CREATED,)
async def create(request: TopicRequest, db: Session = Depends(get_db)):
    topic = db.query(Topic).filter(
        Topic.topic_name == request.topic_name
    ).first()
    # print(topics)
    # Checking if topic already exists
    if topic is not None:
        raise HTTPException(
            status_code=403, detail={
                "status": "failure",
                "message": f"Topic '{request.topic_name}' already exists"
            })
    new_topic: Topic = Topic(topic_name=request.topic_name)
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    # partition of topic
    # logic - divide topic in 4 brokers
    brokers = db.query(Broker).all()
    flag = False
    headers = {"Content-Type": "application/json",
               "accept": "application/json"
               }
    # async with httpx.AsyncClient(follow_redirects=True) as client:
    # try:
    # response = await client.post('http://127.0.0.1:9000/partition/add-partition', headers=headers, json=data)
    data = {
        "topic_name": request.topic_name,
        "partition_id":  1
    }
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = []
        # response = await requests.post(
        #     f'{broker.address}/partition/add-partition', json=data)
        # print(response.json())
        for broker in brokers:
            # print(broker.broker_id)
            # create partion
            partition = Partition(topic_id=new_topic.topic_id,
                                  broker_id=broker.broker_id)
            # add to db
            db.add(partition)
            db.commit()
            db.refresh(partition)       # refresh
            # send to broker using address
            data = {
                "topic_name": new_topic.topic_name,
                "partition_id":  partition.partition_id
            }
            task = asyncio.ensure_future(
                fetch(session, url=f'{broker.address}/partition/add-partition', data=data))
            tasks.append(task)
        # for end
        responses = await asyncio.gather(*tasks)
        print(responses)
        # async with session.post('http://127.0.0.1:9000/partition/add-partition', json=data) as response:
        #     print("Status:", response.status)
        #     res = await response.json()
        #     print(res)
        # try:
        #     response = await client.post(f'{broker.address}/partition/add-partition', headers=headers, json=data)
        #     print(response.text)
        #     # response = await requests.post(
        #     #     f'{broker.address}/partition/add-partition', json=data)
        #     # print(response.json())
        #     # if response.status_code == 201:
        #     #     flag = True
        #     # elif response.status_code == 403:
        #     #     flag: False
        # except:
        #     print('An exception occurred')

    # for end
    print("before partion query")
    return {}
    # if flag:
    #     return {
    #         "status": "success",
    #         "message": f"Topic '{new_topic.topic_name}' created successfully",
    #         "partitions": partitions
    #     }
    # else:
    #     return {
    #         "status": "failure",
    #         "message": f"eror!",
    #         "partitions": partitions
    #     }
