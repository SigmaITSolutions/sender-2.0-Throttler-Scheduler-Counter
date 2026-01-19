PYTHONPATH="./" python3 ./publisher/nats_producer.py 600 2 & 
P1=$!
echo "=====run subcribers======="
PYTHONPATH="./" python3 ./consumer/nats_customer.py  &

P2=$!

#wait $P1 $P2