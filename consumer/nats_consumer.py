from base.nats_connection import NatsConnectionManager,NoServersError,ConnectionClosedError
import asyncio
import json
import time 
from  scheduler.task_scheduler import TaskScheduler
from  scheduler.tasks  import send_scheduled_derfer_mesage_to_adapter
from base.config.config import Decsion
from base.config import config as cfg
from datetime import datetime
### Example Usage

async def message_handler(msg):
    """Callback function to process incoming messages."""
    data = msg.data.decode()
    json_data = json.loads(data)
    decision = json_data['decision']
    if decision == Decsion.ALLOW.value:
        await asyncio.sleep(2)
    if decision == Decsion.DEFER.value:
        task_scheduler = TaskScheduler(cfg.DEFER_QUEUE,cfg.REDIS_HOST)
        send_timestamp = json_data['send_time']
        run_at = datetime.utcfromtimestamp(float(send_timestamp))
        task_scheduler.once_at(run_at,send_scheduled_derfer_mesage_to_adapter,json_data)
                
async def main(queue_group):
    # Example: connect with default settings and automatic reconnect
    nats_manager = NatsConnectionManager(
        servers=cfg.NATS_SERVERS,
        max_reconnect_attempts=-1, # Infinite reconnect attempts
        reconnect_time_wait=5
    )
    try:
        await nats_manager.connect()
        # Subscribe to a subject       
        await nats_manager.subscribe(subject=cfg.NATS_QUEUE,queue_gr=queue_group,callback= message_handler)
        # Keep the program running to receive messages for a short while
        await asyncio.sleep(1) 

    except (NoServersError, ConnectionClosedError, TimeoutError, Exception) as e:
        print(f"Application error: {e}")
    
    try:
        # Keep the connection alive to receive messages indefinitely
        await asyncio.Future() 
    except KeyboardInterrupt:
        # Handle graceful exit
        print("Disconnecting...")
        await nats_manager.close()

        # Ensure the connection is closed gracefully

if __name__ == "__main__":
    # Run the main asynchronous function
    queue_group = "workers"       
    asyncio.run(main(queue_group))
