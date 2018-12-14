# !/usr/bin/python

"""
Task 1: Implementation of the experiment described in the paper with title: 
"From Theory to Experimental Evaluation: Resource Management in Software-Defined Vehicular Networks"
http://ieeexplore.ieee.org/document/7859348/ 
"""

import os
import time
import subprocess
#import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import pylab as plt
from pylab import *
import fnmatch
import operator
import inspect
import traceback
import logging

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, OVSKernelAP
from mininet.link import TCLink
from mininet.log import setLogLevel, debug
from mininet.cli import CLI
#####1
iperf_out_srv = 'iperf_out_srv'
bytes_t_car0 = 'bytes_t_car0'
bytes_r_car3 = 'bytes_r_car3'
bytes_t_car3 = 'bytes_t_car3'
bytes_r_client = 'bytes_r_client'

packets_t_car0 = 'packets_t_car0'
packets_r_car3 = 'packets_r_car3'
packets_t_car3 = 'packets_t_car3'
packets_r_client = 'packets_r_client'

car0_pings_client = 'car0_pings_client'
client_pings_car0 = 'client_pings_car0'
#####2
iperf2_out_srv = 'iperf2_out_srv'
bytes2_t_car0 = 'bytes2_t_car0'
bytes2_r_client = 'bytes2_r_client'

packets2_t_car0 = 'packets2_t_car0'
packets2_r_client = 'packets2_r_client'

car0_pings2_client = 'car0_pings2_client'
client_pings2_car0 = 'client_pings2_car0'
#####3
iperf3_out_srv = 'iperf3_out_srv'
bytes3_t_car0 = 'bytes3_t_car0'
bytes3_r_client = 'bytes3_r_client'

packets3_t_car0 = 'packets3_t_car0'
packets3_r_client = 'packets3_r_client'

car0_pings3_client = 'car0_pings3_client'
client_pings3_car0 = 'client_pings3_car0'

gnet=None

#function pou mas dinei 2 listes Rx,Tx bytes tou ifconfig arxeiou pou eisagoume
def function(lines2read,list1,list2):

	temp1 = []
	temp2 = []
	Rbytes_col = []
	Tbytes_col = []
	for l in lines2read:
		cols = l.split()
	# an einai byte file          RX bytes:11118 (11.1 KB)  TX bytes:648 (648.0 B)
		Rbytes_col.append(cols[1].replace("bytes:","")) 
		Tbytes_col.append(cols[5].replace("bytes:",""))
		#function(argument)
		list1= list(map(int,Rbytes_col))
		list2 = list(map(int,Tbytes_col))
	#~ list1 = temp1
	#~ list2 = temp2
	return list1,list2

#diavazeo file2read kai epistrefei list1 me pososto lanthasmenwn paketwn mexri 2 dekadika
def functionPktT(lines2read,list1):

	total_packets_col = []
	error_packets_col = []
	dropped_packets_col = []
	overr_packets_col = []
	carrier_packets_col = []
	#temp_p_list = [] 
	for l in lines2read:
		cols = l.split()
		total_packets_col.append(cols[1].replace("packets:","")) 
		error_packets_col.append(cols[2].replace("errors:",""))
		dropped_packets_col.append(cols[3].replace("dropped:","")) 
		overr_packets_col.append(cols[4].replace("overruns:","")) 
		carrier_packets_col.append(cols[5].replace("carrier:","")) 
		total_packets_col  = list(map(int,total_packets_col ))
		error_packets_col = list(map(int,error_packets_col))
		dropped_packets_col  = list(map(int,dropped_packets_col ))
		overr_packets_col = list(map(int,overr_packets_col))
		carrier_packets_col  = list(map(int,carrier_packets_col ))
	x = [a+b+c+d for a,b,c,d in zip(error_packets_col, dropped_packets_col,overr_packets_col,carrier_packets_col)]
	x = list(map(float,x))
	xx = [a/b for a,b in zip(x,total_packets_col)]
	list1 = list(map(float,xx))
	list1 = [ round(i * 100,2) for i in list1] #pososto lanthasmenwn paketwn mexri 2 dekadika
	return list1

#diavazeo file2read kai epistrefei list1 me pososto lanthasmenwn paketwn mexri 2 dekadika
def functionPktR(lines2read,list1):
	total_packets_col = []
	error_packets_col = []
	dropped_packets_col = []
	overr_packets_col = []
	frame_packets_col = []
	temp_p_list = [] 
	for l in lines2read:
		cols = l.split()
		total_packets_col.append(cols[1].replace("packets:","")) 
		error_packets_col.append(cols[2].replace("errors:",""))
		dropped_packets_col.append(cols[3].replace("dropped:","")) 
		overr_packets_col.append(cols[4].replace("overruns:","")) 
		frame_packets_col.append(cols[5].replace("frame:","")) 
		total_packets_col  = list(map(int,total_packets_col ))
		error_packets_col = list(map(int,error_packets_col))
		dropped_packets_col  = list(map(int,dropped_packets_col ))
		overr_packets_col = list(map(int,overr_packets_col))
		frame_packets_col  = list(map(int,frame_packets_col ))
	x = [a+b+c+d for a,b,c,d in zip(error_packets_col, dropped_packets_col,overr_packets_col,frame_packets_col)]
	x = list(map(float,x))
	xx = [a/b for a,b in zip(x,total_packets_col)]
	temp_p_list = list(map(float,xx))
	list1 = [ round(i * 100,2) for i in temp_p_list] #pososto lanthasmenwn paketwn mexri 2 dekadika
	return list1

#diavazei file2read kai epistrefei list1,list2,list3 me jitter,packet loss kai bandwidth antistoixa
def functionIperf(lines2read,list1,list2,list3):

	# gia diavasma apo line 8 mexri 
	l = 7 
	j_col = []
	p_loss_col = []
	b_col = []
	while(l < 27):#mexri thn grammh 27
		x = lines2read[l]
		# x = [ 15]  3.0- 4.0 sec   128 KBytes  1.05 Mbits/sec   0.054 ms    0/   89 (0%)
		cols = x.split()
		#end = len(cols)
		#print end
		if (l < 16): # apo 0 - 9 second yparxei mia parapanw sthlh 
			j_col.append(cols[9])# + " " + cols[10])
			p_loss_col.append(round(int(cols[11][:-1])*100/float(cols[12]),2))
			b_col.append(cols[7])
		else:   
			j_col.append(cols[8])#+" "+cols[9])
			p_loss_col.append(round(int(cols[10][:-1])*100/float(cols[11]),2))
			b_col.append(cols[6])
		l+=1
	list1 = j_col
	list2 = p_loss_col
	list3 = b_col
	return list1,list2,list3

#diavazei file2read kai epistrefei list1,list2,list3 me jitter,packet loss kai bandwidth antistoixa
def functionIperf2(lines2read,list1,list2,list3):

	# gia diavasma apo line 8 mexri 
	l = 7 
	j_col = []
	p_loss_col = []
	b_col = []
	while(l < 47 ):#mexri thn grammh 46 (exei allh mia grammh afo to arxeio)
		x = lines2read[l]
		cols = x.split()
		#end = len(cols)
		#print end
		 # apo 0 - 9 second yparxei mia parapanw sthlh 
		if (l < 25):#[  3]  0.0- 1.0 sec   251 KBytes  2.06 Mbits/sec  13.942 ms    0/   88 (0%)
			j_col.append(cols[9])# + " " + cols[10])
			p_loss_col.append(round(int(cols[11][:-1])*100/float(cols[12]),2))
			b_col.append(cols[7])
		else:   #[  3]  9.0-10.0 sec   256 KBytes  2.09 Mbits/sec   5.984 ms    0/   89 (0%)
			j_col.append(cols[8])#+" "+cols[9])
			p_loss_col.append(round(int(cols[10][:-1])*100/float(cols[11]),2))
			b_col.append(cols[6])
		l+=2
	list1 = j_col
	list2 = p_loss_col
	list3 = b_col
	return list1,list2,list3


#diavazei to arxeio file2read kai sth epistrefei list1 me rtt se ms
def functionPing(lines2read,list1):
	l = 1 
	time_col = []
	temp_p_list = [] 
	while (l <  21):
		x = lines2read[l]
		#64 bytes from 192.168.56.101: icmp_seq=5 ttl=64 time=0.043 ms
		cols = x.split()
		time_col.append(cols[6].replace("time=",""))
		l+=1
	temp_p_list = map(float,time_col)
	#list1 = [ round(i,3) for i in temp_p_list]
	list1 = temp_p_list
	#print list1
	return list1
	
#paragei to grafiko gia to prwto peirama	
def graphic1():
	f1 = open('./' + iperf_out_srv, 'r')
	iperf1_lines = f1.readlines()
	f1.close()
    
	f2 = open('./' + bytes_t_car0,'r')
	bytes1_t_car0_lines = f2.readlines()
	f2.close()
    
	f3 = open('./' + bytes_r_car3,'r')
	bytes1_r_car3_lines = f3.readlines()
	f3.close()

	f4 = open('./' + bytes_t_car3,'r')
	bytes1_t_car3_lines = f4.readlines()
	f4.close()
    
	f5 = open('./' + bytes_r_client,'r')
	bytes1_r_client_lines = f5.readlines()
	f5.close()
    
	f6 = open('./' + packets_t_car0,'r')
	packets1_t_car0_lines = f6.readlines()
	f6.close()
    
	f7 = open('./' + packets_r_car3,'r')
	packets1_r_car3_lines = f7.readlines()
	f7.close()
    
	f8 = open('./' + packets_t_car3,'r')
	packets1_t_car3_lines = f8.readlines()
	f8.close()
	
	f9 = open('./' + packets_r_client,'r')
	packets1_r_client_lines = f9.readlines()
	f9.close()
    
	f10 = open('./' + car0_pings_client,'r')
	car0_pings_client_lines = f10.readlines()
	f10.close()
	
	f11 = open('./' + client_pings_car0,'r')
	client_pings_car0_lines = f11.readlines()
	f11.close()
	
	jitter_col = []
	packet_loss_col = []
	bandw_col = []

	car3_r1 = []
	car3_t1 = []
	car3_r2 = []
	car3_t2 = []
	car0_r = []
	car0_t = []
	client_r = []
	client_t = []


	car3_Rerror_pkt = []
	car3_Terror_pkt = []
	car0_error_pkt = []
	client_error_pkt = [] 
	rtt1 = []
	rtt2 = []

	total_time = []
	total_time = np.arange(0,21)

	jitter_col,packet_loss_col,bandw_col = functionIperf(iperf1_lines,jitter_col,packet_loss_col,bandw_col)
	car0_r,car0_t = function(bytes1_t_car0_lines,car0_r,car0_t)
	car3_r2,car3_t2 = function(bytes1_r_car3_lines,car3_r2,car3_t2)
	car3_r1,car3_t1 = function(bytes1_t_car3_lines,car3_r1,car3_t1)
	client_r,client_t = function(bytes1_r_client_lines,client_r,client_t)
	car0_error_pkt = functionPktT(packets1_t_car0_lines,car0_error_pkt)
	car3_Rerror_pkt = functionPktR(packets1_r_car3_lines,car3_Rerror_pkt)
	car3_Terror_pkt = functionPktT(packets1_t_car3_lines,car3_Terror_pkt)
	client_error_pkt = functionPktR(packets1_r_client_lines,client_error_pkt)
	rtt1 = functionPing(car0_pings_client_lines,rtt1)
	rtt2 = functionPing(client_pings_car0_lines,rtt2)

	car0_r.insert(0,0)
	car0_t.insert(0,0)
	car3_r1.insert(0,0)
	car3_t1.insert(0,0)
	car3_r2.insert(0,0)
	car3_t2.insert(0,0)
	client_r.insert(0,0)
	client_t.insert(0,0)
	car0_error_pkt.insert(0,0)
	car3_Terror_pkt.insert(0,0)
	car3_Rerror_pkt.insert(0,0)
	client_error_pkt.insert(0,0)

	#using ifconfig output
	fig_ifconfig = plt.figure(3)
	fig_ifconfig.suptitle('Ifconfig output')

	bX = plt.subplot(311)

	plt.plot(total_time,car0_r,'r',label="car0")
	plt.plot(total_time,car3_r1,'b',label="car3INCOMING")
	plt.plot(total_time,car3_r2,'b.',label="car3OUTCOMING")
	plt.plot(total_time,client_r,'g',label="client")
	plt.xlabel('Time (s)')
	plt.ylabel('Bytes Received')

	# Shrink current axis by 20%
	box = bX.get_position()
	bX.set_position([box.x0, box.y0, box.width * 0.8, box.height])

	# Put a legend to the right of the current axis
	bX.legend(loc='center left', bbox_to_anchor=(1, 0.5))



	plt.subplot(312)
	plt.plot(total_time,car0_t,'r',label="car0")
	plt.plot(total_time,car3_t1,'b-',label="car3INCOMING")
	plt.plot(total_time,car3_t2,'bo',label="car3OUTCOMING")
	plt.plot(total_time,client_t,'g',label="client")
	plt.xlabel('Time (s)')
	plt.ylabel('Bytes Transmitted')

	plt.subplot(313)
	plt.plot(total_time,car0_error_pkt,'r')
	plt.plot(total_time,car3_Terror_pkt,'b-')
	plt.plot(total_time,car3_Rerror_pkt,'bo')
	plt.plot(total_time,client_error_pkt,'g')
	plt.xlabel('Time (s)')
	plt.ylabel('% Packets with errors')

	jitter_col.insert(0,0) #eisagwgh tou 0 sthn prwth thesi ths listas
	bandw_col.insert(0,0)
	packet_loss_col.insert(0,0)
		
	#using iperf output
	fig_iperf = plt.figure(2)
	fig_iperf.suptitle('Iperf output')
	
	plt.subplot(311)
	jitter1_plot = plt.plot(total_time,jitter_col,'r')
	plt.xlabel('Time (s)')
	plt.ylabel('Jitter (ms)')

	plt.subplot(312)
	plt.plot(total_time,bandw_col,'r')
	plt.xlabel('Time (s)')
	plt.ylabel('Bandwidth (Mbits/sec)')

	plt.subplot(313)
	plt.plot(total_time,packet_loss_col,'r')
	plt.xlabel('Time (s)')
	plt.ylabel('Packets lost (%)')


	#using ping output 
	rtt1.insert(0,0)
	rtt2.insert(0,0)

	fig_ping = plt.figure(4)
	fig_ping.suptitle('Ping output')
	
	plt.plot(total_time,rtt1,'r')
	plt.plot(total_time,rtt2,'b')
	plt.xlabel('Time (s)')
	plt.ylabel('Rtt(ms)|red:car0->client | b:client->car0')


	plt.show()
	#~ time.sleep(10)
	#~ plt.clf()
	
	
#paragei to grafiko gia to prwto peirama	
def graphic2():
	f1 = open('./' + iperf2_out_srv, 'r')
	iperf2_lines = f1.readlines()
	f1.close()
    
	f2 = open('./' + bytes2_t_car0,'r')
	bytes2_t_car0_lines = f2.readlines()
	f2.close()
    
	f5 = open('./' + bytes2_r_client,'r')
	bytes2_r_client_lines = f5.readlines()
	f5.close()
    
	f6 = open('./' + packets2_t_car0,'r')
	packets2_t_car0_lines = f6.readlines()
	f6.close()
	
	f9 = open('./' + packets2_r_client,'r')
	packets2_r_client_lines = f9.readlines()
	f9.close()
    
	f10 = open('./' + car0_pings2_client,'r')
	car0_pings2_client_lines = f10.readlines()
	f10.close()
	
	f11 = open('./' + client_pings2_car0,'r')
	client_pings2_car0_lines = f11.readlines()
	f11.close()
	
	jitter_col = []
	packet_loss_col = []
	bandw_col = []

	car0_r = []
	car0_t = []
	client_r = []
	client_t = []


	car0_error_pkt = []
	client_error_pkt = [] 
	rtt1 = []
	rtt2 = []

	total_time = []
	total_time = np.arange(0,21)

	jitter_col,packet_loss_col,bandw_col = functionIperf2(iperf2_lines,jitter_col,packet_loss_col,bandw_col)
	car0_r,car0_t = function(bytes2_t_car0_lines,car0_r,car0_t)
	client_r,client_t = function(bytes2_r_client_lines,client_r,client_t)
	car0_error_pkt = functionPktT(packets2_t_car0_lines,car0_error_pkt)
	client_error_pkt = functionPktR(packets2_r_client_lines,client_error_pkt)
	rtt1 = functionPing(car0_pings2_client_lines,rtt1)
	rtt2 = functionPing(client_pings2_car0_lines,rtt2)

	car0_r.insert(0,0)
	car0_t.insert(0,0)
	client_r.insert(0,0)
	client_t.insert(0,0)
	car0_error_pkt.insert(0,0)
	client_error_pkt.insert(0,0)

	#using ifconfig output
	fig_ifconfig = plt.figure(3)
	fig_ifconfig.suptitle('Ifconfig output')

	bX = plt.subplot(311)

	plt.plot(total_time,car0_r,'r',label="car0")
	plt.plot(total_time,client_r,'g',label="client")
	plt.xlabel('Time (s)')
	plt.ylabel('Bytes Received')

	# Shrink current axis by 20%
	box = bX.get_position()
	bX.set_position([box.x0, box.y0, box.width * 0.8, box.height])

	# Put a legend to the right of the current axis
	bX.legend(loc='center left', bbox_to_anchor=(1, 0.5))



	plt.subplot(312)
	plt.plot(total_time,car0_t,'r',label="car0")
	plt.plot(total_time,client_t,'g',label="client")
	plt.xlabel('Time (s)')
	plt.ylabel('Bytes Transmitted')

	plt.subplot(313)
	plt.plot(total_time,car0_error_pkt,'r')
	plt.plot(total_time,client_error_pkt,'g')
	plt.xlabel('Time (s)')
	plt.ylabel('% Packets with errors')

	jitter_col.insert(0,0) #eisagwgh tou 0 sthn prwth thesi ths listas
	bandw_col.insert(0,0)
	packet_loss_col.insert(0,0)
		
	#using iperf output
	fig_iperf = plt.figure(2)
	fig_iperf.suptitle('Iperf output')
	
	plt.subplot(311)
	jitter1_plot = plt.plot(total_time,jitter_col,'r')
	plt.xlabel('Time (s)')
	plt.ylabel('Jitter (ms)')

	plt.subplot(312)
	plt.plot(total_time,bandw_col,'r')
	plt.xlabel('Time (s)')
	plt.ylabel('Bandwidth (Mbits/sec)')

	plt.subplot(313)
	plt.plot(total_time,packet_loss_col,'r')
	plt.xlabel('Time (s)')
	plt.ylabel('Packets lost (%)')


	#using ping output 
	rtt1.insert(0,0)
	rtt2.insert(0,0)

	fig_ping = plt.figure(4)
	fig_ping.suptitle('Ping output')
	
	plt.plot(total_time,rtt1,'r')
	plt.plot(total_time,rtt2,'b')
	plt.xlabel('Time (s)')
	plt.ylabel('Rtt(ms)|red:car0->client | b:client->car0')


	plt.show()
	#~ time.sleep(10)
	#~ plt.clf()
	
#paragei to grafiko gia to 3o peirama	
def graphic3():
	f1 = open('./' + iperf3_out_srv, 'r')
	iperf3_lines = f1.readlines()
	f1.close()
    
	f2 = open('./' + bytes3_t_car0,'r')
	bytes3_t_car0_lines = f2.readlines()
	f2.close()
    
	f5 = open('./' + bytes3_r_client,'r')
	bytes3_r_client_lines = f5.readlines()
	f5.close()
    
	f6 = open('./' + packets3_t_car0,'r')
	packets3_t_car0_lines = f6.readlines()
	f6.close()
	
	f9 = open('./' + packets3_r_client,'r')
	packets3_r_client_lines = f9.readlines()
	f9.close()
    
	f10 = open('./' + car0_pings3_client,'r')
	car0_pings3_client_lines = f10.readlines()
	f10.close()
	
	f11 = open('./' + client_pings3_car0,'r')
	client_pings3_car0_lines = f11.readlines()
	f11.close()
	
	jitter_col = []
	packet_loss_col = []
	bandw_col = []

	car0_r = []
	car0_t = []
	client_r = []
	client_t = []


	car0_error_pkt = []
	client_error_pkt = [] 
	rtt1 = []
	rtt2 = []

	total_time = []
	total_time = np.arange(0,21)

	jitter_col,packet_loss_col,bandw_col = functionIperf(iperf3_lines,jitter_col,packet_loss_col,bandw_col)
	car0_r,car0_t = function(bytes3_t_car0_lines,car0_r,car0_t)
	client_r,client_t = function(bytes3_r_client_lines,client_r,client_t)
	car0_error_pkt = functionPktT(packets3_t_car0_lines,car0_error_pkt)
	client_error_pkt = functionPktR(packets3_r_client_lines,client_error_pkt)
	rtt1 = functionPing(car0_pings3_client_lines,rtt1)
	rtt2 = functionPing(client_pings3_car0_lines,rtt2)

	car0_r.insert(0,0)
	car0_t.insert(0,0)
	client_r.insert(0,0)
	client_t.insert(0,0)
	car0_error_pkt.insert(0,0)
	client_error_pkt.insert(0,0)

	#using ifconfig output
	fig_ifconfig = plt.figure(3)
	fig_ifconfig.suptitle('Ifconfig output')

	bX = plt.subplot(311)

	plt.plot(total_time,car0_r,'r',label="car0")
	plt.plot(total_time,client_r,'g',label="client")
	plt.xlabel('Time (s)')
	plt.ylabel('Bytes Received')

	# Shrink current axis by 20%
	box = bX.get_position()
	bX.set_position([box.x0, box.y0, box.width * 0.8, box.height])

	# Put a legend to the right of the current axis
	bX.legend(loc='center left', bbox_to_anchor=(1, 0.5))



	plt.subplot(312)
	plt.plot(total_time,car0_t,'r',label="car0")
	plt.plot(total_time,client_t,'g',label="client")
	plt.xlabel('Time (s)')
	plt.ylabel('Bytes Transmitted')

	plt.subplot(313)
	plt.plot(total_time,car0_error_pkt,'r')
	plt.plot(total_time,client_error_pkt,'g')
	plt.xlabel('Time (s)')
	plt.ylabel('% Packets with errors')

	jitter_col.insert(0,0) #eisagwgh tou 0 sthn prwth thesi ths listas
	bandw_col.insert(0,0)
	packet_loss_col.insert(0,0)
		
	#using iperf output
	fig_iperf = plt.figure(2)
	fig_iperf.suptitle('Iperf output')
	
	plt.subplot(311)
	jitter1_plot = plt.plot(total_time,jitter_col,'r')
	plt.xlabel('Time (s)')
	plt.ylabel('Jitter (ms)')

	plt.subplot(312)
	plt.plot(total_time,bandw_col,'r')
	plt.xlabel('Time (s)')
	plt.ylabel('Bandwidth (Mbits/sec)')

	plt.subplot(313)
	plt.plot(total_time,packet_loss_col,'r')
	plt.xlabel('Time (s)')
	plt.ylabel('Packets lost (%)')


	#using ping output 
	rtt1.insert(0,0)
	rtt2.insert(0,0)

	fig_ping = plt.figure(4)
	fig_ping.suptitle('Ping output')
	
	plt.plot(total_time,rtt1,'r')
	plt.plot(total_time,rtt2,'b')
	plt.xlabel('Time (s)')
	plt.ylabel('Rtt(ms)|red:car0->client | b:client->car0')


	plt.show()
	#~ time.sleep(10)
	#~ plt.clf()


def topology():
	"Create a network."
	net = Mininet(controller=Controller, link=TCLink, switch=OVSKernelSwitch, accessPoint=OVSKernelAP)
	global gnet
	gnet = net

	print "*** Creating nodes"
	car = []
	stas = []
	for x in range(0, 4):
		car.append(x)
		stas.append(x)
	for x in range(0, 4):
		car[x] = net.addCar('car%s' % (x), wlans=2, ip='10.0.0.%s/8' % (x + 1), \
		mac='00:00:00:00:00:0%s' % x, mode='b')
    
	eNodeB1 = net.addAccessPoint('eNodeB1', ssid='eNodeB1', dpid='1000000000000000', mode='ac', channel='1', position='80,75,0', range=60)
	eNodeB2 = net.addAccessPoint('eNodeB2', ssid='eNodeB2', dpid='2000000000000000', mode='ac', channel='6', position='180,75,0', range=70)
	rsu1 = net.addAccessPoint('rsu1', ssid='rsu1', dpid='3000000000000000', mode='g', channel='11', position='140,120,0', range=40)
	c1 = net.addController('c1', controller=Controller)
	client = net.addHost ('client')
	switch = net.addSwitch ('switch', dpid='4000000000000000')

	net.plotNode(client, position='125,230,0')
	net.plotNode(switch, position='125,200,0')

	print "*** Configuring wifi nodes"
	net.configureWifiNodes()

	print "*** Creating links"
	net.addLink(eNodeB1, switch)
	net.addLink(eNodeB2, switch)
	net.addLink(rsu1, switch)
	net.addLink(switch, client)

	print "*** Starting network"
	net.build()
	c1.start()
	eNodeB1.start([c1])
	eNodeB2.start([c1])
	rsu1.start([c1])
	switch.start([c1])

	for sw in net.vehicles:
		sw.start([c1])

	i = 1
	j = 2
	for c in car:
		c.cmd('ifconfig %s-wlan0 192.168.0.%s/24 up' % (c, i))
		c.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (c, i))
		c.cmd('ip route add 10.0.0.0/8 via 192.168.1.%s' % j)
		i += 2
		j += 2

	i = 1
	j = 2
	for v in net.vehiclesSTA:
		v.cmd('ifconfig %s-eth0 192.168.1.%s/24 up' % (v, j))
		v.cmd('ifconfig %s-mp0 10.0.0.%s/24 up' % (v, i))
		v.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
		i += 1
		j += 2

	for v1 in net.vehiclesSTA:
		i = 1
		j = 1
		for v2 in net.vehiclesSTA:
			if v1 != v2:
				v1.cmd('route add -host 192.168.1.%s gw 10.0.0.%s' % (j, i))
			i += 1
			j += 2

	client.cmd('ifconfig client-eth0 200.0.10.2')
	net.vehiclesSTA[0].cmd('ifconfig car0STA-eth0 200.0.10.50')

	car[0].cmd('modprobe bonding mode=3')
	car[0].cmd('ip link add bond0 type bond')
	car[0].cmd('ip link set bond0 address 02:01:02:03:04:08')
	car[0].cmd('ip link set car0-eth0 down')
	car[0].cmd('ip link set car0-eth0 address 00:00:00:00:00:11')
	car[0].cmd('ip link set car0-eth0 master bond0')
	car[0].cmd('ip link set car0-wlan0 down')
	car[0].cmd('ip link set car0-wlan0 address 00:00:00:00:00:15')
	car[0].cmd('ip link set car0-wlan0 master bond0')
	car[0].cmd('ip link set car0-wlan1 down')
	car[0].cmd('ip link set car0-wlan1 address 00:00:00:00:00:13')
	car[0].cmd('ip link set car0-wlan1 master bond0')
	car[0].cmd('ip addr add 200.0.10.100/24 dev bond0')
	car[0].cmd('ip link set bond0 up')

	car[3].cmd('ifconfig car3-wlan0 200.0.10.150')

	client.cmd('ip route add 192.168.1.8 via 200.0.10.150')
	client.cmd('ip route add 10.0.0.1 via 200.0.10.150')

	net.vehiclesSTA[3].cmd('ip route add 200.0.10.2 via 192.168.1.7')
	net.vehiclesSTA[3].cmd('ip route add 200.0.10.100 via 10.0.0.1')
	net.vehiclesSTA[0].cmd('ip route add 200.0.10.2 via 10.0.0.4')

	car[0].cmd('ip route add 10.0.0.4 via 200.0.10.50')
	car[0].cmd('ip route add 192.168.1.7 via 200.0.10.50')
	car[0].cmd('ip route add 200.0.10.2 via 200.0.10.50')
	car[3].cmd('ip route add 200.0.10.100 via 192.168.1.8')

	"""plot graph"""
	net.plotGraph(max_x=250, max_y=250)

	net.startGraph()

	# STREAMING commands
	car[0].cmdPrint("cvlc -vvv bunnyMob.mp4 --sout '#duplicate{dst=rtp{dst=200.0.10.2,port=5004,mux=ts},dst=display}' :sout-keep &")
	car[0].cmdPrint("echo $!") # PID of latest bg process
	client.cmdPrint("cvlc rtp://200.0.10.2:5004/bunnyMob.mp4 &")
	client.cmdPrint("echo $!")

	car[0].moveNodeTo('95,100,0')
	car[1].moveNodeTo('80,100,0')
	car[2].moveNodeTo('65,100,0')
	car[3].moveNodeTo('50,100,0')

	os.system('ovs-ofctl del-flows switch')

	time.sleep(3)

	#apply_experiment(car,client,switch,net) # DOKIMH XWRIS FUNCTION
	time.sleep(2)
	print "Applying first phase"
	os.system('ovs-ofctl mod-flows switch in_port=1,actions=output:4')
	os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:1')

	car[0].cmd('ip route add 200.0.10.2 via 200.0.10.50')
	client.cmd('ip route add 200.0.10.100 via 200.0.10.150')
	#me aftes edw tis entoles pane ta mhnymata #gia kapoio logo de tis dexetai mesa apo python 
	#client.cmd('ip route add 200.0.10.100 via 200.0.10.2')
	#car[0].cmd('ip route add 200.0.10.2 via 200.0.10.100')

	CLI(net)#kanw xterm client ,car0 kai tis prosthetw

	#ifconfig output gathering
	#~ t_end = time.time() + 21 #gia 20 seconds 
	#~ print time.time()
	print "ifonfig output gathering"
	t_simulation = 0
	while t_simulation < 20:
		car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % packets_t_car0)
		car[0].cmd('ifconfig bond0 | grep \"TX bytes\" >> %s' % bytes_t_car0)
		car[3].cmd('ifconfig car3-eth0 | grep \"RX packets\" >> %s' % packets_r_car3)
		car[3].cmd('ifconfig car3-eth0 | grep \"RX bytes\" >> %s' % bytes_r_car3)

		car[3].cmd('ifconfig car3-wlan0 | grep \"TX packets\" >> %s' % packets_t_car3)
		car[3].cmd('ifconfig car3-wlan0 | grep \"TX bytes\" >> %s' % bytes_t_car3)
		client.cmd('ifconfig client-eth0 | grep \"RX packets\" >> %s' % packets_r_client)
		client.cmd('ifconfig client-eth0 | grep \"RX bytes\" >> %s' % bytes_r_client)
		time.sleep(1)
		t_simulation=t_simulation+1    

	#iperf output gathering
	client.cmdPrint('iperf -s -u -i 1 > %s &' % iperf_out_srv)
	car[0].cmdPrint('iperf -u -i 1 -t 20 -c 200.0.10.2')
	#client.cmdPrint('sudo kill -9 $!') #skotwnw th diergasia tou iperf ston client
	
	#ping output gathering
	#~ car[3].cmd('ping -t 1 -c 20 200.0.10.100 > %s' % ping_v2v) #ping sto car3->car0
	#~ car[3].cmd('ping -t 1 -c 20 200.0.10.2 > %s' % ping_v2i) #ping sto car3->client
	car[0].cmd('ping -t 1 -c 20 200.0.10.2 > %s' % car0_pings_client)
	client.cmd('ping -t 1 -c 20 200.0.10.100 > %s' % client_pings_car0)
    
	graphic1()
	print "xterm client -> sudo kill -9 <client_iperf_bg_process_PID>"
	CLI(net)

	#end of phase 1 
	print "Moving nodes"
	car[0].moveNodeTo('150,100,0')
	car[1].moveNodeTo('120,100,0')
	car[2].moveNodeTo('90,100,0')
	car[3].moveNodeTo('70,100,0')

	time.sleep(2)
	print "Applying second phase"

	os.system('ovs-ofctl del-flows switch')
	os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
	os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2')
	os.system('ovs-ofctl mod-flows switch in_port=3,actions=output:4')
	os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:3')

	#~ mallon prepei ksana xterm client car0 kai tis parakatw
	#~ client.cmd('route add -host 200.0.10.100 gw 200.0.10.2')
	#~ car[0].cmd('route add -host 200.0.10.2 gw 200.0.10.100')
	#~ telika tis eixe akomh perasmenes apo to prohgoumeno xterm client car0

	print "ifonfig output gathering"
	t_simulation = 0
	while t_simulation < 20:
		car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % packets2_t_car0)
		car[0].cmd('ifconfig bond0 | grep \"TX bytes\" >> %s' % bytes2_t_car0)
		client.cmd('ifconfig client-eth0 | grep \"RX packets\" >> %s' % packets2_r_client)
		client.cmd('ifconfig client-eth0 | grep \"RX bytes\" >> %s' % bytes2_r_client)
		time.sleep(1)
		t_simulation=t_simulation+1    

	print 'iperf output gathering'
	#CLI(net)
	client.cmdPrint('iperf -s -u -i 1 > %s &' % iperf2_out_srv)
	car[0].cmdPrint('iperf -u -i 1 -t 20 -c 200.0.10.2')
	#client.cmdPrint('sudo kill -9 $!') #skotwnw th diergasia tou iperf ston client
	
	print 'ping output gathering'
	#~ car[3].cmd('ping -t 1 -c 20 200.0.10.100 > %s' % ping_v2v) #ping sto car3->car0
	#~ car[3].cmd('ping -t 1 -c 20 200.0.10.2 > %s' % ping_v2i) #ping sto car3->client
	car[0].cmd('ping -t 1 -c 20 200.0.10.2 > %s' % car0_pings2_client)
	client.cmd('ping -t 1 -c 20 200.0.10.100 > %s' % client_pings2_car0)
	

	graphic2()
	time.sleep(2)
    #################################################################################
    
	print "Moving nodes"
	car[0].moveNodeTo('190,100,0')
	car[1].moveNodeTo('150,100,0')
	car[2].moveNodeTo('120,100,0')
	car[3].moveNodeTo('90,100,0')

	time.sleep(2)
	print "Applying third phase"
    
    ################################################################################ 
    #   1) Add the flow rules below and routing commands if needed
	os.system('ovs-ofctl del-flows switch')
	os.system('ovs-ofctl mod-flows switch in_port=2,actions=output:4')
	os.system('ovs-ofctl mod-flows switch in_port=4,actions=output:2')

    #   2) Calculate Network Measurements using IPerf or command line tools(ifconfig)
    #       Hint: Remember that you can insert commands via the mininet
    #       Example: car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % output.data)
	print "*** CLI 3 *** -- check if streaming is happening(eNodeB2 only) (car0 ping client)"
	print "ifonfig output gathering"
	t_simulation = 0
	while t_simulation < 20:
		car[0].cmd('ifconfig bond0 | grep \"TX packets\" >> %s' % packets3_t_car0)
		car[0].cmd('ifconfig bond0 | grep \"TX bytes\" >> %s' % bytes3_t_car0)
		client.cmd('ifconfig client-eth0 | grep \"RX packets\" >> %s' % packets3_r_client)
		client.cmd('ifconfig client-eth0 | grep \"RX bytes\" >> %s' % bytes3_r_client)
		time.sleep(1)
		t_simulation=t_simulation+1    

	print 'iperf output gathering'
	CLI(net)
	client.cmdPrint('iperf -s -u -i 1 > %s &' % iperf3_out_srv)
	car[0].cmdPrint('iperf -u -i 1 -t 20 -c 200.0.10.2')
	#client.cmdPrint('sudo kill -9 $!') #skotwnw th diergasia tou iperf ston client
	
	print 'ping output gathering'
	#~ car[3].cmd('ping -t 1 -c 20 200.0.10.100 > %s' % ping_v2v) #ping sto car3->car0
	#~ car[3].cmd('ping -t 1 -c 20 200.0.10.2 > %s' % ping_v2i) #ping sto car3->client
	car[0].cmd('ping -t 1 -c 20 200.0.10.2 > %s' % car0_pings3_client)
	client.cmd('ping -t 1 -c 20 200.0.10.100 > %s' % client_pings3_car0)

    # Uncomment the line below to generate the graph that you implemented
	graphic3()
#	time.sleep(5) #na prolavei na fortwsei ta figures
    # kills all the xterms that have been opened
#    os.system('pkill xterm')

#    print "*** Running CLI"
	print "last CLI before closing"
	CLI(net)

	print "*** Stopping network"
	net.stop()

if __name__ == '__main__':
	setLogLevel('info')
	try:
		topology()
	except:
		print 'print_exception():'
		exc_type, exc_value, exc_tb = sys.exc_info()
		traceback.print_exception(exc_type,exc_value,exc_tb)
		if gnet != None:
			gnet.stop()
		else:
			print "No network was created..."
	finally:
		os.system('sudo mn -c')
		text = raw_input("Press enter to delete output files")
		os.system('sudo rm bytes*')
		os.system('sudo rm packets*')
        os.system('sudo rm iperf*')
        os.system('sudo rm *pings*')

