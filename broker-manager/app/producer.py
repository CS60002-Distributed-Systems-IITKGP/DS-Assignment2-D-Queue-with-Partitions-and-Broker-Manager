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
from sqlalchemy import desc

get_db = database.get_db

router = APIRouter(
    prefix="/producer",
    tags=['producer']
)


class RegisterProducerRequest(BaseModel):
    topic: str


async def fetch(session: aiohttp.ClientSession, url, data):
    async with session.post(url, json=data) as response:
        res = await response.json()
        stat = response.status
        return {'status': stat, 'response': res}


# Register producer with topics
@router.post('/register')
async def create(request: RegisterProducerRequest, db: Session = Depends(get_db)):
    # check topic in db
    topic = None
    topic = db.query(Topic).filter(
        Topic.topic_name == request.topic).first()
    partitions = []
    if topic is None:
        partitions = []
        # create new topic
        topic = Topic(topic_name=request.topic)
        db.add(topic)
        db.commit()
        db.refresh(topic)
        # partition of topic
        # logic - divide topic in 4 brokers
        brokers = db.query(Broker).all()

        async with aiohttp.ClientSession(trust_env=True) as session:
            tasks = []
            for broker in brokers:
                # print(broker.broker_id)
                # create partion
                partition = Partition(topic_id=topic.topic_id,
                                      broker_id=broker.broker_id)
                # add to db
                db.add(partition)
                db.commit()
                db.refresh(partition)       # refresh
                partitions.append(partition)
                # send to broker using address
                data = {
                    "topic_name": topic.topic_name,
                    "partition_id":  partition.partition_id
                }
                task = asyncio.ensure_future(
                    fetch(session, url=f'{broker.address}/partition/add-partition', data=data))
                tasks.append(task)
            # for end
            responses = await asyncio.gather(*tasks)
            print(responses)
    else:
        partitions = db.query(Partition).filter(
            Partition.topic_id == topic.topic_id).order_by(Partition.created_date).all()

# add producer
    # also add next_partition_id
    new_producer = Producer(topic_id=topic.topic_id,
                            next_partition_id=partitions[0].partition_id)

    db.add(new_producer)
    db.commit()
    db.refresh(new_producer)
    print(new_producer.producer_id)
    return {"status": "success", "producer_id": new_producer.producer_id}


# # posting message


class EnqueueRequest(BaseModel):
    topic: str
    producer_id: int
    message: str
    partition_id: Optional[int] = None


@router.post('/produce')
async def all(request: EnqueueRequest, db: Session = Depends(get_db),):
    producer = db.query(Producer).filter(
        Producer.producer_id == request.producer_id
    ).first()
    if producer is None:
        raise HTTPException(status_code=404, detail={
            "status": "failure",
            "message": f"producer '{request.producer_id}' not found!"
        })
    topic_matched = producer.topics
    # print(topic_matched)
    if (topic_matched.topic_name == request.topic):
        if request.partition_id is not None:
            partition = db.query(Partition).filter(
                Partition.partition_id == request.partition_id).first()
        # get partition data from partition table using next partition id
        else:
            partition = db.query(Partition).filter(
                Partition.partition_id == producer.next_partition_id).first()
            # get partitions from db
            partition_list = db.query(Partition).filter(
                Partition.topic_id == topic_matched.topic_id).order_by(Partition.created_date).all()
            # get index of next_partition_id - using partition_list and next_partition_id <- index + 1
            print(partition_list)
            for i in range(len(partition_list)):
                if partition_list[i].partition_id == producer.next_partition_id:
                    next_partition_pos = i
                    break
            print(next_partition_pos)
            new_index = (next_partition_pos + 1) % len(partition_list)
            print(new_index)
            # next_partition_pos.order_by(desc(Partitionmycol))
            producer.next_partition_id = partition_list[new_index].partition_id
            db.commit()
            db.refresh(producer)
        # get broker data using partition.broker_id
        broker = partition.broker
        # send message to broker - data -- topic_name, parition_id, message
        data = {
            "topic_name": topic_matched.topic_name,
            "partition_id": partition.partition_id,
            "message": request.message

        }
        # send
        async with aiohttp.ClientSession(trust_env=True) as session:
            tasks = []
            url = f'{broker.address}/producer/enqueue'
            async with session.post(url, json=data) as response:
                data = await response.json()

            # task = asyncio.ensure_future(
            #     fetch(session, url=f'{broker.address}/producer/enqueue', data=data))
            # tasks.append(task)
        # getting response in task
        # responses = await asyncio.gather(*tasks)
        print(data)
        return {"status": "success", "responses": data}
    else:
        raise HTTPException(status_code=404, detail={
            "status": "failure",
            "message": f"Topic '{request.topic}' not found!"
        })
