import json
import asyncio
import sys
from base.nats_connection import NatsConnectionManager,NoServersError,ConnectionClosedError
import time 
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


async def run_publisher(counter=0,msg_batch=[],duration=30*60):
    print(f'===Process_{counter}==START')
    nats_manager = NatsConnectionManager(
        servers=["nats://10.0.0.115:4222"],
        max_reconnect_attempts=-1, # Infinite reconnect attempts
        reconnect_time_wait=5
    )
    msg = {
            'process':counter,
            'notify_msg': msg_batch,
            'order':0 
          }
    interval = 0.02
    step_total = int(duration/interval)
    try:
        await nats_manager.connect()
        print(f'Number of packets:{step_total}')
        for i in range(step_total):
            msg['order'] = i
            msg['time'] = time.time()
            decision = "ALLOW"
            if i % 3 != 0:
                decision = "DEFER"
            msg['decision'] = decision     
            json_string = json.dumps(msg)
            bytes_obj = json_string.encode('utf-8')
            ack = await nats_manager.publish("updates",bytes_obj)
        await asyncio.sleep(interval)
    except (NoServersError, ConnectionClosedError, TimeoutError, Exception) as e:
        print(f"Application error: {e}")
    finally:
        await nats_manager.close()
    print(f'===Process_{counter}--{step_total} packages==END')

async def main(msg,duration=300,process=5):
    pub_list =[]
    for i in range(process):
        pub_list.append(run_publisher(i,msg,duration))
    await asyncio.gather(*pub_list)
    #await asyncio.gather(run_publisher(0,msg,duration), run_publisher(1,msg,duration), 
    #                     run_publisher(2,msg,duration),run_publisher(3,msg,duration),run_publisher(4,msg,duration))
if __name__ == '__main__':
    number = 1000
    args = sys.argv
    duration = 60
    process = 1
    if len(args) > 1:
        duration = int(args[1])
        process = int(args[2])
        print(f"***Run time:{duration}---process:{process}")
    msg = list()
    for i in range(number):
        msg = msg + [raw_event_sample]       
    asyncio.run(main(msg,duration=duration,process=process))

