
# Distributed Queue with Partition And Broker Manager
## Contributors
1. Suryawanshi Vivek Bapurao(coderviky) - 22CS60R62
2. Sairaj Das(sairajd044) - 22CS60R30
3. Sahil Mahapatra(dotslashbit) - 22CS60R14
4. Debdutta Mitra(Dmitra1993) - 22CS60R12
5. Sourajit Bhattacharjee(soura1819) - 22CS60R68


## Overview
Multiple producers subscribe to different topics and under those topics they generate log messages asynchronously and there are multiple consumers who are also subscribed to multiple topics and consumed those messages from the queue asynchronously.  
These topics are divided into 4 partitions, each partition are maintained by different brokers. There is a broker manager which acts as inter-communicator between producer consumer and the brokers.


## HTTP APIs
### Register Producer
This operation allows a producer to register for a certain topic with the message queue.For each subscription/registration of a specific topic, unique registration id will be assigned to the producer.If that specific topic is not present then it will create a new topic with the reqested topic name by calling **Create Topic API**.

```python
Method: POST
Endpoint: /producer/register
Params:
    "topic": <string>
Response:
    "status": <string>
    onSuccess:
        - "producer_id": <int>
    onFailure:
        - "message": "Connection failure" // Error message
```

<!-- ## Broker Manager Endpoints -->

### Create Topic
This operation allows to add a new topic to the list of available topics and producer as well as consumer are allowed to subscribe those topics.If that requested topic is already exists in DB, then "topic already exists!" error message will be generated.  
Broker manager accepts the request from producer and consumer, then it'll route it to that broker which is maintaining one partition of that topic if topic already exists, otherwise, it'll create four partitions of the new topic and allot them to each broker.

```python
Method: POST
Endpoint: /topics
Params:
    - "name": <string>
Response:
    onSuccess:
        - "status": "success"
        - "message": <string>
    onFailure:
        - "status": "failure"
        - "message":  "topic already exists!" // error message
```

### List Topics
This operation returns all the available topics present in the DB.If no topics are available, then "no topics found!" error will be generated.
```python
Method: GET
Endpoint: /topics
Params:
    None
Response:
    "status": <string>
    onSuccess:
        - "topics": List[<string>] // List of topic names
    onFailure:
        - "message": "No topics found!" // Error message
``` 

### Register Consumer
This operation allows each consumer to register with a specific topic.A consumer can also register with multiple topics but for each topic registration, a unique registration id will be generated.If consumer tried to register with a topic which is not present in the queue, then error message "topic not found" will be generated.
```python
Method: POST
Endpoint: /consumer/register
Params:
    "topic": <string>
Response:
    "status": <string>
    onSuccess:
        - "consumer_id": <int>
    onFailure:
        - "message": "topic not found" // Error message
```

### Enqueue
This operation enlist a new log message produced by a particular producer of a particular topic producer subscribed. If producer is not subscribed to a topic which it is trying to add message, then "producer not found" error message will be generated else message will be added or appended to the corresponding topic queue.  
In this scenario, broker manager will accept the message from producer.It maintains a database of which topic partition is alloted to which broker and what is the last broker the last message was enqueued.Fetching those details broker manager routes that message to the corresponding broker in round robin fashion.


```python
Method: POST
Endpoint: /producer/produce
Params:
    - "topic": <string>
    - "producer_id": <int>
        - "message": <string> // Log message to enqueue
Response:
    "status": <string>
    onSuccess:
        None
    onFailure:
        - "message": "Producer not found" // Error message
```

### Dequeue
This operation delist a log message from requested topic queue on FCFS basis.For a particular topic, as multiple consumers can be subscribed, so copy of the requested message of a topic will be forward to the consumer so that other consumer can also get the same message from the same topic, if it has been subscribed to.  
If consumer is not subscribed to a topic of which it is trying to get message, then "consumer not found" error message will be generated else message will be forward to the corresponding consumer.  
In this scenario, broker manager will accept the request from consumer and it'll fetch from DB that from which partition the consumer got the message last time according to that it routes the request to the corresponding broker to get the message from DB in round robin fashion.

```python
Method: GET
Endpoint: /consumer/consume
Params:
    - "topic": <string>
    - "consumer_id": <int>
Response:
    "status": <string>
    onSuccess:
        - "message": <string> // Log message
    onFailure:
        - "message": "Consumer not found" // Error message
```

### Size
This operation returns the number of messages still left to read for a particular topic of a consumer.If consumer requested to get the size of a topic which it is not subscribed, then "Consumer not found" error message will be generated.  
Broker manager handle this operation by collecting data from each broker.
```python
Method: GET
Endpoint: /size
Params:
    - "topic": <string>
    - "consumer_id": <int>
Response:
    "status": <string>
    onSuccess:
        - "size": <int>
    onFailure:
        - "message": "Consumer not found" // Error message
```
# Database Design

## Broker Schema

### TopicPartition
TopicPartition table contains three attributes:
1. topic_partition_id (primary key) [auto-generated]
2. topic_name
3. partition_id

### Message
Message table contains four attributes:
1. message_id (primary key)
2. topic_partition_id (foreign key: Topic_Partition.topic_partition_id)
3. message
4. created_date

## Broker Manager Schema

### Topic
Topic table contains two attributes:
1. topic_id (primary key)
2. topic_name

### Producer
Producer table contains three attributes:
1. producer_id (primary key)
2. topic_id (foreign key: Topic.topic_id)
3. next_partition_id (foreign key: Partitions.partition_id)



### Consumer
Consumer table contains three attributes:
1. consumer_id (primary key)
2. topic_id (foreign key: Topic.topic_id)
3. next_partition_id (foreign key: Partitions.partition_id)

### ConsumerPartition
ConsumerPartition table contains three attributes:
1. consumer_id (primary key, foreign key: Consumer.consumer_id)
2. partition_id (primary key, foreign key: Partition.partition_id)
3. last_message_index

### Partition
Partition table contains four attributes:
1. partition_id (primary key)
2. topic_id (foreign key: Topic.topic_id)
3. broker_id (foreign key: Broker.broker_id)
4. created_date [auto-generated]

### Broker
Broker table contains 3 attributes:
1. broker_id (primary key)
2. address
3. hostname






## Tehcnology Used
1. Python3
2. FastAPI
3. Docker
4. PostgreSQL
5. git
6. Github

