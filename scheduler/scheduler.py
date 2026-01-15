from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
#import datetime
from datetime import datetime ,timedelta
from rq.registry import ScheduledJobRegistry


def task_queue_xx(msg):
    print(f'==task_queue:{msg}')
    with open("/Volumes/WorkPlace/Sigma/Sender/sender-2.0-Throttler-Scheduler-Counter/scheduler/demofile.txt", "w") as f:
        f.write(f"Now the file has more content!:{msg}")



#queue = Queue('bar', connection=Redis(host="10.0.0.115"))
#scheduler = Scheduler(queue=queue, connection=queue.connection)
#t1 = datetime.now() + timedelta(minutes=2)
#print(f"=========kk:{t1.strftime("%d/%m/%Y, %H:%M:%S")}")
#job = scheduler.enqueue_at(t1,task_queue_xx,"Hello task queue")
#print("Enqueued job ",job)

#scheduler.enqueue_in(timedelta(minutes=2),task_queue_xx,"Hello task queue")

#registry = ScheduledJobRegistry(queue=queue)


task_queue_xx("xxx")
