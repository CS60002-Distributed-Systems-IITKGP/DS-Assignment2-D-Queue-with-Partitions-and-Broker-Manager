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

get_db = database.get_db

router = APIRouter(
    prefix="/consumer",
    tags=['consumer']
)


class RegisterConumerRequest(BaseModel):
    topic: str


class DenqueueRequest(BaseModel):
    topic: str
    consumer_id: int


# Register consumer with topics
@router.post('/register', status_code=status.HTTP_201_CREATED,)
def create(request: RegisterConumerRequest, db: Session = Depends(get_db)):
    # check topic in db
    topic = db.query(Topic).filter(Topic.topic_name == request.topic).first()
    if topic is None:
        raise HTTPException(status_code=404, detail={
            "status": "failure",
            "message": f"Topic '{request.topic}' not found!"
        })
    # new consumer with topic_id
    new_consumer = Consumer(topic_id=topic.topic_id)
    db.add(new_consumer)
    db.commit()
    db.refresh(new_consumer)
    # get partitions from db
    partitions = db.query(Partition).filter(
        Partition.topic_id == topic.topic_id).order_by(Partition.created_date).all()

    # create new entry in consumer_partition table for each partition
    for partition in partitions:
        consumer_partition = ConsumerPartition(
            consumer_id=new_consumer.consumer_id, partition_id=partition.partition_id)
        db.add(consumer_partition)
    print(f"partitions[0].partition_id : {partitions[0].partition_id}")
    new_consumer.next_partition_id = partitions[0].partition_id
    db.commit()
    # print(new_consumer.consumer_id)
    return {"status": "success", "consumer_id": new_consumer.consumer_id}


@router.post('/consume')
async def all(request: DenqueueRequest, db: Session = Depends(get_db),):
    consumer = db.query(Consumer).filter(
        Consumer.consumer_id == request.consumer_id
    ).first()
    if consumer is None:
        raise HTTPException(status_code=404, detail={
            "status": "failure",
            "message": f"conumer'{request.consumer_id}' not found!"
        })

    topic_matched = consumer.topic
    # print(topic_matched)
    if (topic_matched.topic_name == request.topic):

        # get next message index from consumer_partition using next partiotion id
        consumer_partition = db.query(ConsumerPartition).filter(ConsumerPartition.consumer_id == consumer.consumer_id,
                                                                ConsumerPartition.partition_id == consumer.next_partition_id).first()

        # send request to broker with partition id
        partition_to_consume = db.query(Partition).filter(
            Partition.partition_id == consumer.next_partition_id).first()
        print(consumer.next_partition_id)
        print(partition_to_consume.partition_id)

        broker = partition_to_consume.broker

        data = {
            "partition_id": consumer.next_partition_id,
            "topic_name": request.topic,
            "last_message_index": consumer_partition.last_message_index
        }
        print(data)
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json"}
        # change
        # get partitions from db
        partition_list = db.query(Partition).filter(
            Partition.topic_id == topic_matched.topic_id).order_by(Partition.created_date).all()
        # get index of next_partition_id - using partition_list and next_partition_id <- index + 1
        # print(partition_list)
        for i in range(len(partition_list)):
            if partition_list[i].partition_id == consumer.next_partition_id:
                next_partition_pos = i
                break
        # print(next_partition_pos)
        new_index = ((next_partition_pos + 1) % len(partition_list))
        # print(new_index)
        # next_partition_pos.order_by(desc(Partitionmycol))
        consumer.next_partition_id = partition_list[new_index].partition_id
        db.commit()
        db.refresh(consumer)

        # send
        url = f'{broker.address}/consumer/dequeue'
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.post(url, headers=headers, json=data) as response:
                res = await response.json(content_type="application/json")
                stat = response.status
        # print(res)
        # return {"status": "success", "responses": res}
        # check status code
        if (stat == 200):
            # update last message index + 1
            consumer_partition.last_message_index = consumer_partition.last_message_index + 1
            db.commit()
            db.refresh(consumer_partition)
            return {"status": "success", "responses": res}
        else:
            return {"response": res}

    else:
        raise HTTPException(status_code=404, detail={
            "status": "failure",
            "message": f"Topic '{request.topic}' not found!"
        })
