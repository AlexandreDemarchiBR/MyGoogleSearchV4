#!/bin/bash
# envia arqivos para os workers
for ip in $(cat workers); do
    expect setup_env.exp $ip
done