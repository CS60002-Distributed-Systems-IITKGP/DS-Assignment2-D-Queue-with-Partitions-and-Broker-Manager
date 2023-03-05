from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core import database
from models import Message, TopicPartition
from pydantic import BaseModel

get_db = database.get_db

router = APIRouter(
    prefix="/producer",
    tags=['producer']
)


class RegisterProducerRequest(BaseModel):
    topic: str


class EnqueueRequest(BaseModel):
    topic: str
    producer_id: int
    message: str

# # posting message


@router.post('/produce')
def all(request: EnqueueRequest, db: Session = Depends(get_db),):
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
        # add message for topic
        new_message = Message(
            topic_id=topic_matched.topic_id, message=request.message)
        
        ##TODO: Route it to broker
        
        
        # db.add(new_message)
        # db.commit()
        # db.refresh(new_message)
        return {"status": "success"}
    else:
        raise HTTPException(status_code=404, detail={
            "status": "failure",
            "message": f"Topic '{request.topic}' not found!"
        })


# Register producer with topics
@router.post('/register')
def create(request: RegisterProducerRequest, db: Session = Depends(get_db)):
    # check topic in db
    topic = db.query(Topic).filter(
        Topic.topic_name == request.topic).first()
    if topic is None:
        # create new topic
        new_topic = Topic(topic_name=request.topic)


        #TODO: Route it to broker for creating new topic

        # db.add(new_topic)
        # db.commit()
        # db.refresh(new_topic)
        # topic = new_topic
    new_producer = Producer(topic_id=topic.topic_id)
    
    #TODO: Route it to broker
    
    
    # db.add(new_producer)
    # db.commit()
    # db.refresh(new_producer)
    # print(new_producer.producer_id)
    return {"status": "success", "producer_id": new_producer.producer_id}