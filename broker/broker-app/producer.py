
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

# topic_name, parition_id, message
class EnqueueRequest(BaseModel):
    topic_name: str
    partition_id: int
    message: str

# # posting message


@router.post('/enqueue')
def all(request: EnqueueRequest, db: Session = Depends(get_db),):
    # get partition data from TopicPartition
    print(request)
    topic_partition = db.query(TopicPartition).filter(TopicPartition.topic_name == request.topic_name,TopicPartition.partition_id == request.partition_id).first()
    if topic_partition is None:
        raise HTTPException(status_code=404, detail={
            "status": "failure",
            "message": f"topic '{request.topic_name}' with partition {request.partition_id} not found!"
        })
    # add message using topicpartition.topic_partition_id
    message = Message(topic_partition_id = topic_partition.topic_partition_id,message = request.message)
    db.add(message)
    db.commit()
    db.refresh(message)
    return {"status": "success"}


# # Register producer with topics
# @router.post('/register')
# def create(request: RegisterProducerRequest, db: Session = Depends(get_db)):
#     # check topic in db
#     topic = db.query(Topic).filter(
#         Topic.topic_name == request.topic).first()
#     if topic is None:
#         # create new topic
#         new_topic = Topic(topic_name=request.topic)
#         db.add(new_topic)
#         db.commit()
#         db.refresh(new_topic)
#         topic = new_topic
#     new_producer = Producer(topic_id=topic.topic_id)
#     db.add(new_producer)
#     db.commit()
#     db.refresh(new_producer)
#     # print(new_producer.producer_id)
#     return {"status": "success", "producer_id": new_producer.producer_id}
