#!/bin/bash

now=$( date '+%F_%H:%M:%S' )
log=dumpResults_$now.log
sudo sysctl -a | grep tcp_congestion_control >> $log
while true; do
  date
  iperf3 -c starlink-surrey.duckdns.org -t 60 -i1 -p 4213 -R >> $log
  sleep 240
done
