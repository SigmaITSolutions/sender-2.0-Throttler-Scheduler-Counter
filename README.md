# sender-2.0-Throttler-Scheduler-Counter
Throttler-Scheduler-Counter solutions (RD)


## Option A: RabbitMQ + Redis (not official)

**Components**:

- RabbitMQ = message broker.
- Redis = counters store + delay queue (optional).

```mermaid
flowchart LR
    DE["Decision Engine"] -->|DecisionResult| Sender["Sender Orchestrator"]
    Sender -->|ALLOW/DEFER/BLOCK| TS["Throttler & Scheduler"]

    TS -->|ALLOW -> push job| RMQ["RabbitMQ<br/>dispatch queues"]
    RMQ -->|work items| PushWorker["Push Dispatch Worker"]
    PushWorker --> PPG["Push Provider (PPG)"]

    TS -->|DEFER -> delayed job| RedisDelay["Redis ZSET<br/>delay_queue"]
    Scheduler["Delay Scheduler Worker"] --> RedisDelay
    Scheduler --> Sender

    DE --> RedisCounters["Redis Cluster<br/>frequency_counters"]
```

## Option B: NATS JetStream + Redis (not official)

**Components**:

- NATS + JetStream = event/stream & work queue.
- Redis = counters.

```mermaid
flowchart LR
    DE["Decision Engine"] --> Sender["Sender Orchestrator"]
    Sender -->|DecisionBatchResult| NATS["NATS JetStream<br/>subject: sender.decisions"]

    subgraph TSGroup["Throttler & Scheduler Workers"]
        TS1["TS Worker #1"]
        TS2["TS Worker #2"]
    end

    NATS --> TS1
    NATS --> TS2

    TS1 -->|ALLOW->dispatch batch| ProviderQ["NATS subject: sender.dispatch.push"]
    ProviderQ --> PushWorker["Push Dispatch Worker"]
    PushWorker --> PPG["Push Provider"]

    TS1 -->|DEFER with DeliverAfter| NATSDelay["NATS delayed message"]
    NATSDelay --> TS1

    DE --> Redis["Redis Cluster<br/>frequency_counters"]
```
# Throttler and Scheduler Diagrams
## Sequence Diagram
![System Sequence Diagram](docs/ThrottlerAndScheduler-Seq-Diagram.png)


**Deploy and Simulation Step**
1. Run up nats and redis servers by docker-compose
   > docker-compose up redis nats
2. Install must have python lib by pip command
   >pip3 install -r requirements.txt
3. Update ip of nats and redis in file base/config/config.py  
4. Run consumer and publisher nats by script nats_process.sh
   >chmod u+x nats_process.sh
   >source nats_process.sh
5. Run scheduler worker to perfom jobs at their execution time 
   >chmod u+x worker-wakeup.sh
   >source worker-wakeup.sh

6. Optional run rq-dashboard to see and monitor information of scheduler
   >rq-dashboard -u redis://10.0.0.115:6379       