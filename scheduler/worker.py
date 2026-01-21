from rq import Worker, Queue
from redis import Redis
from base.config import config as cfg
redis = Redis(host=cfg.REDIS_HOST)
queue = Queue(name=cfg.DEFER_QUEUE,connection=redis)
#if __name__ == '__main__':
worker = Worker(queues=[queue], connection=redis)
worker.work(with_scheduler=True)