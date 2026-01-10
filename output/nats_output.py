import asyncio
from nats.aio.client import Client as NATS
import json
import time 
async def run_subscriber():
    nc = NATS()
    await nc.connect("nats://10.0.0.115:4222")

    async def message_handler(msg):
        subject = msg.subject
        data = msg.data.decode()
        json_data = json.loads(data)
        order = json_data['order']
        process = json_data['process']
        send_time = json_data['time']
        received_time = time.time()
        delta = received_time - send_time
        print(f"{process}|{order}|{delta}")    
    failed_count = 0 
    # Subscribe to the 'updates' subject
    try:
        await nc.subscribe("updates", cb=message_handler)
        print("Subscribed to 'updates' subject, waiting for messages...")
    except Exception:
        failed_count = failed_count + 1
        print(failed_count)
             

    # Keep the connection alive
    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        await nc.close()

if __name__ == '__main__':
    asyncio.run(run_subscriber())
