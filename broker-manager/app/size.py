# from fastapi import APIRouter, Depends, status, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from core import database
# from models import Producer, Consumer, Topic, Message
# from pydantic import BaseModel

# get_db = database.get_db

# router = APIRouter(
#     prefix="/size",
#     tags=['size']
# )


# class SizeRequest(BaseModel):
#     topic: str
#     consumer_id: int


# @router.get('/')
# def all(request: SizeRequest, db: Session = Depends(get_db),):
#     consumer = db.query(Consumer).filter(
#         Consumer.consumer_id == request.consumer_id
#     ).first()
#     if consumer is None:
#         raise HTTPException(status_code=404, detail="consumer not found")
#     # error_flag = True
#     topic_matched = consumer.topics
#     # print(consumer.topics)
#     if (topic_matched.topic_name == request.topic):
#         # taking out messages for topic
#         consumer_messages = db.query(Message).filter(
#             Message.topic_id == topic_matched.topic_id
#         ).all()
#         # message = consumer_messages[consumer.last_message_index]
#         size = len(consumer_messages) - consumer.last_message_index
#         return {"status": "success", "size": size}
#     else:
#         raise HTTPException(status_code=404, detail={
#             "status": "failure",
#             "message": f"Topic '{request.topic}' not found!"
#         })
