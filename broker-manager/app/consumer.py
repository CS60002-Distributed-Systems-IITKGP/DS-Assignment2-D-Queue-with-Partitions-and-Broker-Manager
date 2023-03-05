# from fastapi import APIRouter, Depends, status, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from core import database
# from models import Producer, Consumer, Topic, Message
# from pydantic import BaseModel

# get_db = database.get_db

# router = APIRouter(
#     prefix="/consumer",
#     tags=['consumer']
# )


# class RegisterConumerRequest(BaseModel):
#     topic: str


# class DenqueueRequest(BaseModel):
#     topic: str
#     consumer_id: int


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


# @router.get('/consume')
# def all(request: DenqueueRequest, db: Session = Depends(get_db),):
#     consumer = db.query(Consumer).filter(
#         Consumer.consumer_id == request.consumer_id
#     ).first()
#     if consumer is None:
#         raise HTTPException(status_code=404, detail={
#             "status": "failure",
#             "message": f"conumer'{request.consumer_id}' not found!"
#         })
#     # error_flag = True
#     topic_matched = consumer.topics
#     # print(topic_matched)
#     if (topic_matched.topic_name == request.topic):
#         # taking out messages for topic
#         consumer_messages = db.query(Message).filter(
#             Message.topic_id == topic_matched.topic_id
#         ).all()
#         msg_list_length = len(consumer_messages)
#         # consumer.last_message_index = 0
#         index = consumer.last_message_index
#         # print(index)
#         size = msg_list_length - consumer.last_message_index
#         if size == 0:
#             raise HTTPException(status_code=404, detail={
#                 "status": "failure",
#                 "message": f"No Messages for Topic '{request.topic}' "
#             })
#         # print(consumer_messages)
#         message = consumer_messages[index]
#         # print(message.message)
#         consumer.last_message_index = index + 1
#         db.commit()
#         return {"status": "success", "message": message.message}
#     else:
#         raise HTTPException(status_code=404, detail={
#             "status": "failure",
#             "message": f"Topic '{request.topic}' not found!"
#         })
