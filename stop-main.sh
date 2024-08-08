#!/bin/bash

# Check if the PID file exists
if [ -f rpyc_main.pid ]; then
    # Read the PID from the file
    PID=$(cat rpyc_main.pid)
    echo "Stopping Main server with PID $PID..."
    
    # Kill the process
    kill $PID
    
    # Remove the PID file
    rm rpyc_main.pid

    echo "Main server stopped."
else
    echo "No PID file found. Is the Main server running?"
fi
