PYTHONPATH="./" python3 ./input/nats_jetstream_producer.py 600 2 & 
P1=$!
echo "=====run subcribers======="
PYTHONPATH="./" python3 ./output/nats_jetstream_customer.py &

P2=$!

#wait $P1 $P2