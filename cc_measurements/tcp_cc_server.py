
import os
import time
import signal
import subprocess
from subprocess import check_output
from datetime import datetime
import socket

localIP     = "starlink-surrey.duckdns.org"
localPort   = 20007
bufferSize  = 1024


# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

cc_count = 0
iperf_session_length = 600 #10 minutes
while(True):
	bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
	message = bytesAddressPair[0]
	address = bytesAddressPair[1]
	clientMsg = "Message from Client:{}".format(message)
	clientIP  = "Client IP Address:{}".format(address)
	dt = datetime.now()
	cc_count = clientMsg.split("_")[1]
	ts = clientMsg.split("_")[2]
	print cc_count, ts
	cc = ""
	if int(cc_count) < 6:
		if int(cc_count) == 1:
			cc="CUBIC"
			result = check_output(['sysctl', '-w', 'net.ipv4.tcp_congestion_control=cubic'])
                        cc_name = result.split("=")[1].strip()

		if int(cc_count) == 2:
                        cc="BBR"
			result = check_output(['sysctl', '-w', 'net.ipv4.tcp_congestion_control=bbr'])
                        cc_name = result.split("=")[1].strip()

		if int(cc_count) == 3:
                        cc="VEGAS"
                        result = check_output(['sysctl', '-w', 'net.ipv4.tcp_congestion_control=vegas'])
                        cc_name = result.split("=")[1].strip()

		if int(cc_count) == 4:
                        cc="VENO"
                        result = check_output(['sysctl', '-w', 'net.ipv4.tcp_congestion_control=veno'])
                        cc_name = result.split("=")[1].strip()

		if int(cc_count) == 5:
                        cc="RENO"
                        result = check_output(['sysctl', '-w', 'net.ipv4.tcp_congestion_control=reno'])
                        cc_name = result.split("=")[1].strip()

		year, month, day = str(dt).split(" ")[0].split("-")
                hour, minute, second = str(dt).split(" ")[1].split(":")
                filename = year+"_"+month+"_"+day+"_"+hour+"_"+minute+"_"+second

		print cc_name
		print ts
                cmd = "tcpdump -i wlp0s20f3 -w tcp_cc_resuts/pcap_files/tcp_SERVER_"+cc_name+"_"+str(ts)+"_.pcap"
                pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
                time.sleep(iperf_session_length+50)
                os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

	print(clientMsg)
	print(clientIP)
