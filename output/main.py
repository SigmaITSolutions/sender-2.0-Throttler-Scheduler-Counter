from base.rabbitmq import RabbitMQ
import json 
import time
def callback(ch, method, properties, body):
    data = body.decode('utf8')
    json_data = json.loads(data)
    order = json_data['order']
    process = json_data['process']
    send_time = json_data['sendtime']
    received_time = time.time()
    delta = received_time - send_time
    print(f"{process}|{order}|{delta}")    

rabbitmq = RabbitMQ()
rabbitmq.consume('push.queue',callback)