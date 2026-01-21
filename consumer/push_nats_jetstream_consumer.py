import asyncio
import nats
from asyncio import TimeoutError
from nats.js.errors import FetchTimeoutError
from base.config import config as cfg 
from base.config.config import Decsion
from scheduler.task_scheduler import TaskScheduler
import json 
from datetime import datetime
from scheduler.tasks import send_scheduled_derfer_mesage_to_adapter
class ProcessorWorker:
    def __init__(self, nats_url, redis_host):
        self.nats_url = nats_url
        self.redis_host = redis_host
        self.nc = nats.NATS()
        self.js = None
        self.task_manager = None
        self.connected = False

    async def connect(self):
        """Connect to both NATS and Redis."""
        # Connect NATS
        await self.nc.connect(servers=self.nats_url)
        self.js = self.nc.jetstream()
        
        # Connect Redis (Async)
        self.task_manager = TaskScheduler(queue_name=cfg.DEFER_QUEUE,host=cfg.REDIS_HOST)
        print("Connected to NATS and TaskManager.")
        self.connected = True

    async def start_worker(self, stream="TASKS", subject="tasks.>", durable="result_worker"):
        """Pull tasks from NATS and save results to Redis."""
        if not self.connected:
            await self.connect()
        sub = await self.js.pull_subscribe(subject=subject, durable=durable, stream=stream)
    
        print(f"====Worker listening on {subject}...")
        while True:
            try:
                msgs = await sub.fetch(batch=cfg.BATCH_SIZE, timeout=5)
                for msg in msgs:
                    # 1. Process the task
                    data = msg.data.decode()
                    json_data = json.loads(data)
                    order = json_data['order']
                    print(f'Nats consumer is consuming the order_{order}')
                    decision = json_data['decision']
                    if decision == Decsion.ALLOW.value:
                        self.process_task()
                    if decision == Decsion.DEFER.value:
                        tta = json_data['tta']
                        run_at = datetime.fromtimestamp(tta)
                        self.task_manager.once_at(run_at,send_scheduled_derfer_mesage_to_adapter,json_data)
                    await msg.ack()
                    
            except TimeoutError as te:
                print(f'Timeout error {te}')
                continue
            except Exception as e:
                print(f"Error: {e}\n")
                

    async def process_task(self, raw_data):
        """Your heavy processing logic here."""
        await asyncio.sleep(1) # Simulate work
        return {"status": "completed", "processed_at": "2026-01-20"}

    async def close(self):
        await self.nc.drain()
        await self.redis.close()

if __name__ == "__main__":
    worker = ProcessorWorker(cfg.NATS_SERVERS, cfg.REDIS_URL)
    try:
        #asyncio.run(worker.connect())
        asyncio.run(worker.start_worker(stream=cfg.NATS_STREAM,subject=cfg.NATS_PUSH_CHANNEL,durable=cfg.NATS_DURRABLE))
    except KeyboardInterrupt:
        asyncio.run(worker.close())