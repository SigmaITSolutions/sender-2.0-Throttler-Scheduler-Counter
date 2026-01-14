from redis import Redis
from rq import Queue
import datetime as dt
from datetime import timedelta, datetime
from tasks import send_reminder

# 1. Connect to Redis
redis_conn = Redis(host='192.168.1.100', port=6379)
queue = Queue('default', connection=redis_conn)

def run_schedule():
    # Example A: Run once after a delay (e.g., in 10 seconds)
    #queue.enqueue_in(timedelta(minutes=2), send_reminder, "user@example.com", "John")
    specific_time = datetime.now(dt.UTC) + timedelta(minutes=1)
    queue.enqueue_at(specific_time, send_reminder, "user@example.com", "John")
    print("Jobs have been scheduled!")

if __name__ == "__main__":
    run_schedule()