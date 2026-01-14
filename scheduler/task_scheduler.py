from redis import Redis
from rq import Queue, Repeat
from datetime import timedelta, datetime
from typing import Callable, Any, Optional

class TaskScheduler:
    def __init__(self, queue_name: str = 'default', host: str = 'localhost', port: int = 6379):
        # 1. Initialize Redis connection and Queue
        self.connection = Redis(host=host, port=port)
        self.queue = Queue(queue_name, connection=self.connection)

    def once_in(self, delay_seconds: int, func: Callable, *args, **kwargs):
        """Schedule a job to run once after a delay."""
        return self.queue.enqueue_in(
            timedelta(seconds=delay_seconds), 
            func, 
            *args, 
            **kwargs
        )

    def once_at(self, run_at: datetime, func: Callable, *args, **kwargs):
        """Schedule a job to run once at a specific UTC time."""
        return self.queue.enqueue_at(run_at, func, *args, **kwargs)

    def repeat_every(self, interval_seconds: int, func: Callable, times: Optional[int] = None, *args, **kwargs):
        """
        Schedule a repeating task.
        :param times: Number of times to repeat. None means forever.
        """
        return self.queue.enqueue(
            func,
            args=args,
            kwargs=kwargs,
            repeat=Repeat(times=times, interval=interval_seconds)
        )

    def cancel_job(self, job_id: str):
        """Remove a job from the scheduled registry."""
        job = self.queue.fetch_job(job_id)
        if job:
            job.delete()
            return True
        return False