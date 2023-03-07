from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import func, UniqueConstraint

# TopicPartition - id  topic_name  partition_id

# Message - id  message  topic_partition_id


class TopicPartition(Base):
    __tablename__ = 'topicpartitions'
    __table_args__ = (UniqueConstraint("topic_name", "partition_id"),)

    topic_partition_id = Column(
        Integer, primary_key=True, index=True)  # auto generate

    topic_name = Column(String, )  # 2 column unique
    partition_id = Column(Integer)


class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True, index=True)
    topic_partition_id = Column(
        Integer, ForeignKey('topicpartitions.topic_partition_id'))
    message = Column(String)
    created_date = Column(DateTime, server_default=func.now())

    topic_partitions = relationship("TopicPartition", backref="messages")


# class Topic(Base):
#     __tablename__ = 'topics'

#     topic_id = Column(Integer, primary_key=True, index=True)
#     topic_name = Column(String)


# class Producer(Base):
#     __tablename__ = 'producers'

#     producer_id = Column(Integer, primary_key=True, index=True)
#     topic_id = Column(Integer, ForeignKey('topics.topic_id'))

#     topics = relationship("Topic", backref="producers")


# class Consumer(Base):
#     __tablename__ = 'consumers'

#     consumer_id = Column(Integer, primary_key=True, index=True)
#     topic_id = Column(Integer, ForeignKey('topics.topic_id'))

#     last_message_index = Column(Integer, default=0)

#     topics = relationship("Topic", backref="consumers")


# class Message(Base):
#     __tablename__ = 'messages'

#     message_id = Column(Integer, primary_key=True, index=True)
#     topic_id = Column(Integer, ForeignKey('topics.topic_id'))
#     message = Column(String)
#     created_date = Column(DateTime, server_default=func.now())

#     topics = relationship("Topic", backref="messages")
