#!/bin/bash

now=$( date '+%F_%H:%M:%S' )
log=dumpResults_$now.log


while true; do
  now=$( date '+%F_%H:%M:%S' )
  echo $now | tr -d "\n"; 
  /home/starlink-1/go/bin/grpcurl -plaintext -d {\"get_status\":{}} 192.168.100.1:9200 SpaceX.API.Device.Device/Handle | grep -a 'boresightAzimuthDeg\|boresightElevationDeg\|popPingLatencyMs' | sed 's/^.*: //' | tr -d '\n' && echo -e "\n"
  sleep 0.85;
done

