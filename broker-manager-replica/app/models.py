from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import func
import enum
from sqlalchemy import Enum

# Broker Manager


class BrokerStatusEnum(enum.Enum):
    ACTIVE = 'active'
    FAILED = 'failed'
    IDLE = 'idle'


class Topic(Base):
    __tablename__ = 'topics'

    topic_id = Column(Integer, primary_key=True, index=True)
    topic_name = Column(String)


class Producer(Base):
    __tablename__ = 'producers'

    producer_id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))

    next_partition_id = Column(Integer, ForeignKey('partitions.partition_id') )

    # round_number++;  round_number = round_number % partitions_count  (0 to n-1)
    # to get partition id from ordered list
    round_number = Column(Integer, default=0)

    topics = relationship("Topic", backref="producers")
    partition = relationship("Partition", backref="producers")


class Consumer(Base):
    __tablename__ = 'consumers'

    consumer_id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))

    next_partition_id = Column(Integer, ForeignKey('partitions.partition_id'))

    # round_number++;  round_number = round_number % partitions_count  (0 to n-1)
    # to get partition id from ordered list
    # round_number = Column(Integer, default=0)

    topic = relationship("Topic", backref="consumers")
    # partition = relationship("Partition", backref="consumers")


# ConsumerPartitionData - id conumer_id  partiton_id→  last_message_index
class ConsumerPartition(Base):
    __tablename__ = 'consumerpartitions'

    consumer_id = Column(Integer, ForeignKey(
        'consumers.consumer_id'), primary_key=True)
    partition_id = Column(Integer, ForeignKey(
        'partitions.partition_id'), primary_key=True)

    last_message_index = Column(Integer, default=0)  # for perticular partition

    consumer = relationship("Consumer", backref="consumer_partioions_data")
    partition = relationship("Partition", backref="consumer_partioions_data")


class Partition(Base):
    __tablename__ = 'partitions'

    partition_id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))

    broker_id = Column(Integer, ForeignKey('brokers.broker_id'))
    created_date = Column(DateTime, server_default=func.now())
    
    topics = relationship("Topic", backref="partitions")
    broker = relationship("Broker", backref="partitions")


# BrokerData -  id  address
class Broker(Base):
    __tablename__ = 'brokers'

    broker_id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False, unique=True)
    hostname = Column(String)

    active = Column(Enum(BrokerStatusEnum), default=BrokerStatusEnum.ACTIVE)


# Producer -  id  topic_id→   next_partion_id

# Consumer -  id  topic_id→  next_partion_id   round_number

# Topic  -  id  topic_name

# Partition  -  id  topic_id→  broker_id→

# BrokerData -  id  address
