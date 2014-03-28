'''
vars.py
9/29/13

@author: Brandon Charlesworth
@contact: bjcworth@bu.edu

A simple interface class for keeping track of variables across modules. 

'''
# array of acceptable measurement types for connection setup phase
mtypes = ['rtt','tput']
# keep track of measurement type specified in CSP by client
mtype = 'null'
# White space
ws = ' '
# keep track of message size indicated in CSP by client
msize = 0
# keep track of current probe iteration indicated in MP by client
curprob = 0
# keep track of last probe iteration received from client in MP
lastprob = 0
# keep track of what the current probe should be, by setting equal to lastprobe+1 after each echo
corprob = 1
# keep track of max probes indicated in CSP by client
maxprob = 0
# keep track of delay specified in CSP by client
mdelay = 0
# keep track of payload specified in MP to compare with msize from CSP
payload = 0