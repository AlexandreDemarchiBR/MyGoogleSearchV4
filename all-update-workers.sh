#!/bin/bash
# envia arqivos para os workers
for ip in $(cat workers); do
    expect remote_update.exp worker_service.py $ip
    expect remote_update.exp main_service.py $ip
done