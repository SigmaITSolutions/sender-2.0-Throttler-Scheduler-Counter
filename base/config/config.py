import os
from urllib.parse import urljoin

from environs import Env
from marshmallow.validate import Range
from enum import Enum
NATS_SERVERS=["nats://10.0.0.115:4222"]
REDIS_HOST = "10.0.0.115"
NATS_QUEUE = "msg_queue"
DEFER_QUEUE="defer_queue"

class Decsion(Enum):
    ALLOW ='ALLOW'
    DEFER = 'DEFER'
    DROP ='DROP'

