#!/bin/bash

HOST=0.0.0.0
PORT=18861
echo "Starting Main server on $HOST:$PORT..."
python3 main_service.py --host $HOST

# Save the PID of the RPyC server to a file
echo $! > rpyc_main.pid

echo "Main server started with PID $(cat rpyc_main.pid)"
