#!/bin/bash
# envia arqivos para os workers
for line in $(cat workers); do
    expect send_file.exp worker_service.py $line
    expect send_file.exp main_service.py $line
done