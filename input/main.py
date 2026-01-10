from base.rabbitmq import RabbitMQ
import json 
import time
import multiprocessing as mp
import sys
render_params = {
            "message": "Polsat Box Go",
            "subject": "Dzień dobry",
            "link": "https://polsatboxgo.pl/start",
            "push_portal_icon": "http://ipla.pluscdn.pl/p/versions/qv/qvzmuxb42qr1n2zc8tquf7gvzwf459ig/pbg_push.webp",
        }
template_name = "test_template"
expire_date = "2022-04-01T15:00:00Z"
portal = "pbg"
raw_event_sample = {
            "id": "6e794ab3-fdb8-45a5-87a0-5c170aeb4b5a-testPBG-something",
            "emissionDate": "2022-03-24T13:37:55Z",
            "name": "JsonRpcOverAmqpEvent",
            "originator": "jack",
            "priority": 4,
            "data": {
                "method": "sendPush",
                "params": {
                    "type": "user_id",
                    "portal": portal,
                    "renderParams": render_params,
                    "receivers": "xyz",
                    "templateName": template_name,
                    "expireDate": expire_date,
                },
            },
        }


def rabbitmq_msg(counter=0,msg_batch=[],rabbitmq=None,duration=30*60):
    print(f'===Process_{counter}==START')
    rabbitmq = RabbitMQ()    
    msg = {
            'process':counter,
            'notify_msg': msg_batch
        }
    t1 = time.time()
    count = 0
    interval = 0.02
    step_total = int(duration/interval)
    for i in range(step_total):
        count = count + 1
        msg['order'] = count
        send_time = time.time()
        msg['sendtime'] = send_time
        json_string = json.dumps(msg)
        bytes_obj = json_string.encode('utf-8')
        rabbitmq.publish('push.queue',bytes_obj)
        print(f'{counter}|{count}|{send_time}')
        time.sleep(0.02)
    rabbitmq.close()    
    print(f'===Process_{counter}--{count} packages==END')
    

if __name__ == "__main__":
    number = 1000
    args = sys.argv
    duration = 0
    process = 5 
    if len(args) > 1:
        duration = int(args[1])
        process = int(args[2])
        print(f"***Run time:{duration}--process:{process}")

    msg = list()
    for i in range(number):
        msg = msg + [raw_event_sample]
    
    mp_process = list() 
    for i in range(process):
        process = mp.Process(name=f'Process-{i}', target=rabbitmq_msg, args=(i,msg,duration))
        mp_process.append(process)
    
    for pc in mp_process:
        pc.start()
    for pc in mp_process:
        pc.join()