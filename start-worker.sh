#!/bin/bash

HOST=0.0.0.0
PORT=18862
echo "Starting Worker server on $HOST:$PORT..."
source bin/activate
python3 worker_service.py --host $HOST & disown

# Save the PID of the RPyC server to a file
echo $! > rpyc_worker.pid

echo "Worker server started with PID $(cat rpyc_worker.pid)"
sleep 1 # resolve o $ não aparecendo (precisamos para o expect)
echo