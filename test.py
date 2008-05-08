#!/usr/bin/env python

"""This script keeps track of execution of tests"""

import time,sys
from socket import gethostname

LOG = 'test.log'

def div(n,m):
    return (n/m,n%m)

def human_time(t):
    days,t = div(t,5184000)
    hours,t = div(t,216000)
    mins,t = div(t,3600)
    secs = t
    return (days,hours,mins,secs)

def str_time(t):
    days,hours,mins,secs = human_time(t)
    s = []
    if days:
        s.append(str(days)+'d')
    if hours:
        s.append(str(hours)+'h')
    if mins:
        s.append(str(mins)+'m')
    s.append(str(secs)+'s')
    return ' '.join(s)

def main():
    
    if sys.argv[1:]:
        code = [x.strip() for x in file(argv[1]).readlines()]
    else:
        code = []
    log = []

    print 'Insert code (and a comment):'
    try:
        while True:
            code.append(raw_input())
    except EOFError:
        pass
    
    begin_time = time.time()
    log.append('Begin time: '+time.ctime(begin_time))
    log.append('Task:')
    log += ['*   '+x for x in code]
    log.append('-----')

    file(LOG,'a').writelines([x+'\n' for x in log])

    print "I'm working :-)"
    exec('\n'.join(code))
    finish_time = time.time()
    total_time = int(finish_time-begin_time)

    log = []
    log.append('Begin at: '+time.ctime(begin_time))
    log.append('Finish at: '+time.ctime(finish_time))
    log.append('Hostname: '+gethostname())
    if total_time>59:
        log.append('Total time: ' + str_time(total_time))
    log.append('Total time (secs): '+str(total_time))
    log.append('-----')

    file(LOG,'a').writelines([x+'\n' for x in log])
    
    if '--sms' in sys.argv[1:] or '-s' in sys.argv[1:]:
        import netfinity
        client = netfinity.Client('the9ull6070','trustlet')
        sms = 'Task finished: '+str_time(total_time)+' '+log[2]
        #if the first line of code is a comment it'll send
        if code[0].strip()[0]=='#':
            sms += ' Comment: '+code[0].strip()[1:].strip()
        
        for i in xrange(3):
            try:
                if client.sendMsg(','.join([x.strip() for x in file('phoneNumbers').readlines()]),sms[:160]) > 0:
                    break
            except IOError:
                print "save destination numbers in phoneNumbers file (one number per line)"
        

if __name__=="__main__":
    main()
