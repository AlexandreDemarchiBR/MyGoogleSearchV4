#!/bin/bash
# Testa se as portas estão abertas ou não
for ip in $(cat workers); do
    nmap -p 18862 $ip | grep -e report -e 18862
done