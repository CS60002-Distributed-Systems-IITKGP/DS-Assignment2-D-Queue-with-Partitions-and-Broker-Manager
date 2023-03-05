# from fastapi import APIRouter, Depends, status, HTTPException
# from sqlalchemy.orm import Session
# from typing import List
# from core import database
# from models import Producer, Consumer, Topic, Message
# from pydantic import BaseModel

# get_db = database.get_db

# router = APIRouter(
#     prefix="/topics",
#     tags=['topics']
# )


# class TopicRequest(BaseModel):
#     topic_name: str


# @router.get('/')
# def all(db: Session = Depends(get_db),):
#     topics = db.query(Topic).filter(
#         # Topic.topic_name == ''
#     ).all()
#     if len(topics) == 0:
#         raise HTTPException(status_code=404, detail="No topics found")
#     topic_list = []
#     for topic in topics:
#         topic_list.append(topic.topic_name)
#     return {"topics": topic_list}


# @router.post('/', status_code=status.HTTP_201_CREATED,)
# def create(request: TopicRequest, db: Session = Depends(get_db)):
#     topic = db.query(Topic).filter(
#         Topic.topic_name == request.topic_name
#     ).first()
#     # print(topics)
#     # Checking if topic already exists
#     if topic is not None:
#         raise HTTPException(
#             status_code=404, detail={
#                 "status": "failure",
#                 "message": f"Topic '{request.topic_name}' already exists"
#             })
#     # for topic in topics:
#     #     if topic.request == request:
#     #         raise HTTPException(
#     #             status_code=404, detail={
#     #                 "status": "failure",
#     #                 "message": f"Topic '{request}' already exists"
#     #             })
#     new_topic = Topic(topic_name=request.topic_name)
#     db.add(new_topic)
#     db.commit()
#     db.refresh(new_topic)
#     return {
#         "status": "success",
#         "message": f"Topic '{new_topic.topic_name}' created successfully"
#     }
