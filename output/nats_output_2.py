import asyncio
from nats.aio.client import Client as NATS
from nats.js.api import ConsumerConfig

import json
import time 
import nats 
async def run_subscriber(worker_name):
    print("=====Worker1 START\n")
    
    nc = await nats.connect("nats://10.0.0.115:4222")
    js = nc.jetstream()
    async def message_handler(msg):
        data = msg.data.decode()
        json_data = json.loads(data)
        order = json_data['order']
        process = json_data['process']
        send_time = json_data['time']
        received_time = time.time()
        delta = received_time - send_time
        print(f"{worker_name}|{process}|{order}|{delta}")    
    try:
        await js.subscribe("mobile.push",queue="workers" ,cb=message_handler)
        while True:
            await asyncio.sleep(0.02)
    except Exception:
        failed_count = failed_count + 1
        print(failed_count)
    print("=====Worker1 END\n")
         

    # Keep the connection alive
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        await nc.close()

if __name__ == '__main__':
    worker_name = "Nats worker 2"    
    asyncio.run(run_subscriber(worker_name))
