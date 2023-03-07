from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core import database
from models import Message, TopicPartition
from pydantic import BaseModel

get_db = database.get_db

router = APIRouter(
    prefix="/consumer",
    tags=['consumer']
)


class DenqueueRequest(BaseModel):
    partition_id: int
    topic_name: str
    last_message_index: int


@router.post('/dequeue')
def all(request: DenqueueRequest, db: Session = Depends(get_db),):
    # get topic_partition from db
    topic_partition = db.query(TopicPartition).filter(
        TopicPartition.partition_id == request.partition_id,
        TopicPartition.topic_name == request.topic_name).first()

    # get message list from db
    message_list = db.query(Message).filter(
        Message.topic_partition_id == topic_partition.topic_partition_id).order_by(Message.created_date).all()

    print(message_list)

    # get message
    # new_index = request.last_message_index+1
    print(request.last_message_index)
    if request.last_message_index < len(message_list):
        message = message_list[request.last_message_index]
    else:
        raise HTTPException(status_code=404, detail={
            "status": "failure",
            "message": f"message not found!"
        })

    if message is not None:
        return {"message": message}
    else:
        raise HTTPException(status_code=404, detail={
            "status": "failure",
            "message": f"message not found!"
        })


# # Register consumer with topics
# @router.post('/register', status_code=status.HTTP_201_CREATED,)
# def create(request: RegisterConumerRequest, db: Session = Depends(get_db)):
#     # check topic in db
#     topic = db.query(Topic).filter(Topic.topic_name == request.topic).first()
#     if topic is None:
#         raise HTTPException(status_code=404, detail={
#             "status": "failure",
#             "message": f"Topic '{request.topic}' not found!"
#         })
#     new_consumer = Consumer(topic_id=topic.topic_id)
#     db.add(new_consumer)
#     db.commit()
#     db.refresh(new_consumer)
#     # print(new_consumer.consumer_id)
#     return {"status": "success", "consumer_id": new_consumer.consumer_id}
