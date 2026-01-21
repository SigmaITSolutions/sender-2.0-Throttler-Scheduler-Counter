import asyncio
from nats.js.api import StreamConfig
import nats
from base.config import config as cfg
from base.config.config import Decsion 
import sys 
import json
import datetime as dt
from datetime import datetime,timedelta
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
    nc = await nats.connect(servers=cfg.NATS_SERVERS)
    js = nc.jetstream()
    await js.add_stream(StreamConfig(name=cfg.NATS_STREAM, subjects=[cfg.NATS_PUSH_CHANNEL]))
    msg = {
            'process':counter,
            'notify_msg': msg_batch,
            'order':0,
            'decsion':Decsion.ALLOW.value
          }
    interval = 0.01
    step_total = int(duration/interval)
    
    print(f'Number of packets:{step_total}')
    for i in range(step_total):
        order = i + step_total*counter 
        
        msg['order'] = order # i + step_total*counter 
        if order%3 ==0:
            msg['decision']=Decsion.DEFER.value
            send_time = datetime.now()+ timedelta(minutes=2)
            msg['tta']= send_time.timestamp()            
        json_string = json.dumps(msg)
        bytes_obj = json_string.encode('utf-8')
        ack = await js.publish(cfg.NATS_PUSH_CHANNEL,bytes_obj)
        print(f"Order:{order}-Ack: Stream {ack.stream}, Sequence {ack.seq}")
        await asyncio.sleep(interval)

    #await nc.close()
    print(f'===Process_{counter}--{step_total} packages==END')

async def main(msg,duration=300,process=5):
    pub_list =[]
    for i in range(process):
        pub_list.append(run_publisher(i,msg,duration))
    await asyncio.gather(*pub_list)
    
if __name__ == '__main__':
    number = 10
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
