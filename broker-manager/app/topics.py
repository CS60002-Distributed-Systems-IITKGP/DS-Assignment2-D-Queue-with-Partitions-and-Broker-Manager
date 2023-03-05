from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from core import database
from models import Producer, Consumer, Topic, ConsumerPartition, Partition, BrokerStatusEnum, Broker
from pydantic import BaseModel
import requests

get_db = database.get_db

router = APIRouter(
    prefix="/topics",
    tags=['topics']
)


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

    for broker in brokers:
        # create partion
        partition = Partition(topic_id=new_topic.topic_id,
                              broker_id=broker.broker_id)
        # add to db
        db.add(partition)
        db.commit()
        # refresh
        db.refresh(partition)
        # send to broker using address
        data = {
            "topic_name": new_topic.topic_name,
            "partition_id":  partition.partition_id
        }
        try:
            response = await requests.post(
                f'{broker.address}/partition/add-partition', json=data)
            print(response.json())
            if response.status_code == 201:
                flag = True
            elif response.status_code == 403:
                flag: False
        except:
            print('An exception occurred')

    # for end

    partitions = db.query(Partition).filter(
        Partition.topic_id == new_topic.topic_id)
    if flag:
        return {
            "status": "success",
            "message": f"Topic '{new_topic.topic_name}' created successfully",
            "partitions": partitions
        }
    else:
        return {
            "status": "failure",
            "message": f"eror!",
            "partitions": partitions
        }
