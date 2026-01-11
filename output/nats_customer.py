from base.nats_connection import NatsConnectionManager,NoServersError,ConnectionClosedError
import asyncio
import json
import time 

### Example Usage

async def message_handler(msg):
    """Callback function to process incoming messages."""
    subject = msg.subject
    data = msg.data.decode()
    json_data = json.loads(data)
    order = json_data['order']
    process = json_data['process']
    send_time = json_data['time']
    received_time = time.time()
    delta = received_time - send_time
    print(f"|{process}|{order}|{delta}|")    

async def main(queue_group):
    # Example: connect with default settings and automatic reconnect
    nats_manager = NatsConnectionManager(
        servers=["nats://10.0.0.115:4222"],
        max_reconnect_attempts=-1, # Infinite reconnect attempts
        reconnect_time_wait=5
    )
    try:
        await nats_manager.connect()
        # Subscribe to a subject       
        await nats_manager.subscribe("updates",queue_gr=queue_group,callback= message_handler)
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
