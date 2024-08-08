#!/bin/bash
# reinicia tudo
bash stop-main.sh
for ip in $(cat workers); do
    expect remote_stop.exp $ip
done

for ip in $(cat workers); do
    expect remote_start.exp $ip
done
bash start-main.sh