import os
from urllib.parse import urljoin

from environs import Env
from marshmallow.validate import Range
from enum import Enum
NATS_SERVERS=["nats://192.168.1.100:4222"]
REDIS_HOST = "192.168.1.100"
NATS_QUEUE = "msg_queue"
DEFER_QUEUE="defer_queue"

class Decsion(Enum):
    ALLOW ='ALLOW'
    DEFER = 'DEFER'
    DROP ='DROP'

