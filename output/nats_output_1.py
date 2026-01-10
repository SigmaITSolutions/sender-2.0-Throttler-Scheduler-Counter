import asyncio
from nats.aio.client import Client as NATS
from nats.js.api import ConsumerConfig
import nats
import json
import time 
async def run_subscriber(worker_name):
   
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
        await js.subscribe("events.updates", cb=message_handler)
    except Exception:
        failed_count = failed_count + 1
        print(failed_count)
    #print("=====Worker1 END\n")     

    # Keep the connection alive
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        await nc.close()

if __name__ == '__main__':
    worker_name = "Nats worker 1"    
    asyncio.run(run_subscriber(worker_name))
