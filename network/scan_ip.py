#!/usr/bin/env python
# -*- encoding:utf-8 -*-

'''
a scan ip function by scapy
'''
 
from scapy.all import *
from time import ctime,sleep
import threading 
import init

conf.verb=0
TIMEOUT = 2 
 
def pro(ip, cc, handle):
    global dict
    dst = ip + str(cc)
    packet = IP(dst=dst, ttl=20)/ICMP()
    reply = sr1(packet, timeout=TIMEOUT)
    if reply:
        print reply.src,' is online'
        tmp = [1, reply.src]
        handle.write(reply.src + '\n')
        #handle.write(reply.src+" is online"+"\n")
 
def main():
    threads=[]
    start, end = init.parseconf('conf.ini', 'scanrange')
    s = int(start[(start.rfind('.') + 1):])
    e = int(end[(end.rfind('.') + 1):])
    ip = start[:(start.rfind('.') + 1)]
    f=open('ip.log','w+')
    for i in range(s, e):
        t=threading.Thread(target=pro,args=(ip,i,f))
        threads.append(t)
    print "main Thread begins at ",ctime()
    for t in threads :
        t.start()
    for t in threads :
        t.join()
    print "main Thread ends at ",ctime()
 
if __name__=="__main__" :
    main()
