#!/usr/bin/env python

"""
echoserver.py
9/29/13

@author: Brandon Charlesworth
@contact: bjcworth@bu.edu
ID: U20809812




"""

import socket
import sys
import time
from vars import *

host = ''
port = int(sys.argv[1])
backlog = 5
size = 32768


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)


# connection setup phase (check for length of string sent, proper measurement type, and at least 10 probes)
def csp(t):
    global mtypes, mtype, msize, maxprob, mdelay
    t = t.split()
    if(len(t)!=5):
        client.send("404 ERROR: Invalid Length Specified for Connection Setup Message")
        client.close()
    else:
        if t[1]:
            if(t[1] not in mtypes):
                client.send("404 ERROR: Invalid Mtype Specified for Connection Setup Message")
                client.close()
            else:
                mtype = t[1]
        if t[2]:
            if(t[2]<10):
                client.send( "404 ERROR: Invalid Number of Probes Specified for Connection Setup Message")
                client.close()
            else:
                maxprob = int(t[2])
        if t[3]:
            msize = int(t[3])
        
        mdelay = int(t[4])
        client.send("200 OK: Ready \n")

# Measurement Phase (Make sure current probe is the one that should follow the last, and that we dont
# exceed the max probes indicated in the CSP)

def mp(t):
    global curprob, corprob, lastprob, payload, msize
    data = t
    t = t.split()
    if(len(t)!=3):
        print "404 ERROR: Invalid Length Specified for Measurement Message"
        client.close()
    else:
        if t[1]:
            curprob = int(t[1])
          
            if((curprob != corprob) or (curprob != lastprob+1) or (curprob > maxprob)):
                client.send( "404 ERROR: Invalid Probe Sequence Number Specified for Measurement Message")
                client.close()
            else:
                lastprob = curprob
                corprob+=1
        if t[2]:
            payload = t[2]
            if(len(payload)!= msize):
                client.send( "404 ERROR: Payload Specified Does Not Match Msize from Connection Setup")
                client.close()
                
       # If delay indicated, sleep for that many  secs
        if(mdelay>0):
            print "Sleeping for ", mdelay, " secs before echoing..."
            time.sleep(mdelay)
        client.send(data)
        print "Msg echoed! \n"
        
# connection termination phase (make sure length is correct, terminate if correct message received)
        
def ctp(t):
    t = t.split()
    if(len(t)!=1):
        client.send("404 ERROR: Invalid Length Specified for Connection Termination Message")
        client.close()
    else: 
        print "Terminating connection...\n"
        client.send("200 OK: Closing Connection \n")
        client.close()
        

# wait on client and direct to the correct phase if data received
client, address = s.accept()
while 1:
    data = client.recv(size)
    if data:
        print "Msg received from client\n"
        header = data[0]
        if header=='s':
            csp(data)
            continue
        if header=='m':
            mp(data)
            continue
        if header=='t':
            ctp(data)
