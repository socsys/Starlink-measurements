import os
import time
import signal
import subprocess
from subprocess import check_output
from datetime import datetime
import socket
from threading import Thread

msgFromClient       = "From Client - Start Recording"
bytesToSend         = str.encode(msgFromClient)
serverAddressPort   = ("starlink-surrey.duckdns.org", 20007)
bufferSize          = 1024


iperf_session_length = 540 #9 minutes

def start_tcpdump():
	cmd = "tcpdump -i eth0 -s96 -w /home/starlink-1/kassem/measurements_scripts/tcp_cc_results/pcap_files/tcp_RECEIVER_"+cc_name+"_"+str(ts)+"_.pcap"
        pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
	time.sleep(iperf_session_length+51)
	os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
	print "tcpdumpis killed"

cc_count = 0
while(True):
	cc_count = cc_count + 1
	if cc_count == 1:
		cc = "CUBIC"
		result = check_output(['sysctl', '-w', 'net.ipv4.tcp_congestion_control=cubic'])
		cc_name = result.split("=")[1].strip()

	if cc_count == 2:
		cc == "BBR"
		result = check_output(['sysctl', '-w', 'net.ipv4.tcp_congestion_control=bbr'])
                cc_name = result.split("=")[1].strip()

	if cc_count == 3:
		cc == "VEGAS"
                result = check_output(['sysctl', '-w', 'net.ipv4.tcp_congestion_control=vegas'])
                cc_name = result.split("=")[1].strip()

	if cc_count == 4:
		cc == "VENO"
                result = check_output(['sysctl', '-w', 'net.ipv4.tcp_congestion_control=veno'])
                cc_name = result.split("=")[1].strip()

	if cc_count == 5:
		cc == "RENO"
                result = check_output(['sysctl', '-w', 'net.ipv4.tcp_congestion_control=reno'])
                cc_name = result.split("=")[1].strip()

	dt = datetime.now()
	ts = time.time()

        print cc_name
	print ts

	t1 = Thread(target=start_tcpdump)
	t1.start()

	msgFromClient       = "From Client - Start Recording_"+str(cc_count)+"_"+str(ts)
        bytesToSend         = str.encode(msgFromClient)

	UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	UDPClientSocket.sendto(bytesToSend, serverAddressPort)
	print("Message Sent!")
	if cc_count == 5:
		cc_count = 0

	time.sleep(1)

	iperfcmd = "iperf3 -c starlink-surrey.duckdns.org -i1 -t"+str(iperf_session_length)+" -R >> /home/starlink-1/kassem/measurements_scripts/tcp_cc_results/iperf_data/dump_iperf_"+str(cc_name)+"_"+str(ts)
	os.system(iperfcmd)
	time.sleep(53)
	print("iperf done!")
