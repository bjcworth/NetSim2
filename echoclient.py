#!/usr/bin/env python

"""
echoclient.py
9/29/13

@author: Brandon Charlesworth
@contact: bjcworth@bu.edu
ID: U20809812



"""

import socket
import sys
import time
import math
from vars import maxprob, msize, mdelay, mtype, ws

host = sys.argv[1]
port = int(sys.argv[2])
size = 32768
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sent = 0.0
rcvd = 0.0
a_rtt = 0.0
a_tput = 0.0


# Connection Setup Phase (CSP)
def csp():
    global mtype, msize, maxprob, mdelay
    print "\n_______________________________"
    print "        [Connection Phase] \n_______________________________\n"
    print "Connecting to server..."
    # connect to port
    s.connect((host,port))
    print "Connected! \n"
    msg = raw_input("Enter a message to send to server (<s> <Mtype> <# Probes> <Msg Size> <Delay>): \n> ")
    s.send(msg)
    print "Msg sent! \n"
    data = s.recv(size)
    if data:
        print "Received From Server: ", data, "\n"
        msg = msg.split()
        mtype = msg[1]
        maxprob = int(msg[2])
        msize = int(msg[3])
        mdelay = int(msg[4])
        mp(mtype, msize, maxprob)

# Measurement Phase (MP)
def mp(type, payload, max):
    global sent, rcvd, a_rtt, a_tput, size
    print "_______________________________"
    print "        [Measurement Phase] \n _______________________________\n"
    # Fill the message with the payload specified from CSP
    butt = ""; msg = ""; rtt = []; tput = []; s_rtt = 0.0
    while (len(butt) < payload):
        butt += '1'
    # Send the number of probes indicated in CSP
    for y in range(1,max+1):
        msg = str("m"+ws+str(y)+ws+butt)
        print "\nSending..."
        # Send msg, record time sent
        s.send(msg); sent = 1000* (time.time())
        print "Msg sent! \n"
        data = s.recv(size)
        
        # If msg echoed from server...
        if data:
            # Store time echoed, record rtt for that probe
            rcvd = 1000.0* (time.time()); s_rtt = rcvd-sent; rtt.insert(y-1,s_rtt)
            print "Echoed From Server: ", data, "\n", "rtt: ", s_rtt, " ms"
            if type == 'tput':
                # record tput, accounting for actual msg size when calculating (header+ws+payload) 
                tput.insert(y-1, (len(msg)/1024.0)/(rtt[y-1]/1000.0))
                print "tput: ", tput[y-1], "KBps"
                # if we are at the last probe
            if y == max:
                # print summary of tput and rtt
                print "\nrtt summary (ms): ", rtt
                a_rtt = (math.fsum(rtt))/max
                print "avg rtt: ", a_rtt, " ms\n"
                if type == 'tput':
                    print "tput summary (KBps): ", tput
                    a_tput = (math.fsum(tput))/max
                    print "avg tput: ", a_tput, " KBps\n"

    print "Leaving Protocol Phase... \n"
    ctp()

# Connection Termination Phase (CTP)
def ctp():
    print "_______________________________"
    print "        [Termination Phase] \n_______________________________\n"
    # send termination msg
    msg = "t"+ws
    print "Sending termination message..."
    s.send(msg)
    print "Msg sent! \n"
    data = s.recv(size)
    # if echoed...
    if data:
        print "Received From Server:", #data
    print "Terminating... \n"
    # terminate
    s.close()
    

if __name__ == '__main__':
    csp()
