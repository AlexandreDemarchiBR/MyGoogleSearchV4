#!/bin/bash

# Check if the PID file exists
if [ -f rpyc_worker.pid ]; then
    # Read the PID from the file
    PID=$(cat rpyc_main.pid)
    echo "Stopping Worker server with PID $PID..."
    
    # Kill the process
    kill $PID
    
    # Remove the PID file
    rm rpyc_worker.pid

    echo "Worker server stopped."
else
    echo "No PID file found. Is the Worker server running?"
fi
