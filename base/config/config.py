import os
from urllib.parse import urljoin

from environs import Env
from marshmallow.validate import Range
from enum import Enum
NATS_SERVERS=["nats://192.168.1.100:4222"]
REDIS_HOST = "192.168.1.100"
NATS_QUEUE = "msg_queue"
DEFER_QUEUE="defer_queue"
NATS_PUSH_CHANNEL="push.channel"
NATS_MAIL_CHANNEL="mail.channel"
NATS_SMS_CHANNEL="sms.channel"
NATS_DURRABLE="server_1"
BATCH_SIZE=100
NATS_STREAM="nats_stream"
REDIS_URL="redis://192.168.1.100:6379"


class Decsion(Enum):
    ALLOW ='ALLOW'
    DEFER = 'DEFER'
    DROP ='DROP'

