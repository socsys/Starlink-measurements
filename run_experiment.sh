#!/bin/bash

# Check if gedit is running
# -x flag only match processes whose name (or command line if -f is
# specified) exactly match the pattern. 


declare -a arr=("abrDynamic" "abrThroughput")

for i in "${arr[@]}"
do

	x=1
	while [ $x -le 6 ]
	do
		echo "Iteration $x and abr Alogrithm $i"
		python video_streaming_autoScript.py $i $x 
  		x=$(( $x + 1 ))
		while pgrep -f "python video_streaming_autoScript.py" > /dev/null
		do
    			sleep 10
		done
	done
done

