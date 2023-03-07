from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core import database
from models import Message, TopicPartition
from pydantic import BaseModel


get_db = database.get_db

router = APIRouter(
    prefix="/partition",
    tags=['topics']
)


class PartionRequest(BaseModel):
    topic_name: str
    partition_id: int


@router.post('/add-partition', status_code=status.HTTP_201_CREATED,)
def create(request: PartionRequest, db: Session = Depends(get_db)):
    partition = db.query(TopicPartition).filter(
        TopicPartition.topic_name == request.topic_name, TopicPartition.partition_id == request.partition_id
    ).first()
    # Checking if partion already exists
    if partition is not None:
        raise HTTPException(
            status_code=403, detail={
                "status": "failure",
                "message": f"Partition with topic '{request.topic_name}' and id '{request.partition_id}' already exists"
            })
    new_partition = TopicPartition(
        topic_name=request.topic_name, partition_id=request.partition_id)
    db.add(new_partition)
    db.commit()
    db.refresh(new_partition)
    return {
        "status": "success",
        "message": f"Partition with topic '{request.topic_name}' and id '{request.partition_id}' created successfully with id {new_partition.topic_partition_id}"
    }


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
