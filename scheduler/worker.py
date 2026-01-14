from rq import Worker, Queue
from redis import Redis

redis = Redis(host="192.168.1.100")
queue = Queue(name='defer',connection=redis)
if __name__ == '__main__':
    worker = Worker(queues=[queue], connection=redis)
    worker.work(with_scheduler=True)