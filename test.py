#!/usr/bin/env python

"""This script keeps track of execution of tests"""

import time,sys,os
from socket import gethostname

LOG = 'test.log'

def div(n,m):
    return (n/m,n%m)

def human_time(t):
    from time import gmtime #(tm_year, tm_mon, tm_mday, tm_hour, tm_min,
                            # tm_sec, tm_wday, tm_yday, tm_isdst)
    tt = gmtime(t)
    #(days,hours,mins,secs)
    return (t/24/60/60,tt[3],tt[4],tt[5])

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

def test():
    print "test"
    print str_time(15)
    print str_time(3600)
    print str_time(13600)
    print str_time(113600)
    print str_time(12336000)
    

def main():
    
    if '--help' in sys.argv[1:]:
        print "USAGE: ./test.py [-s|--sms] [file common instructions]"
        return
    if 'test' in sys.argv[1:]:
        test()
        return
    if sys.argv[1:]:
        filename = None
        for f in sys.argv[1:]:
            if f[0]!='-':
                filename=f
                break
        if filename:
            code = [x[-1]=='\n' and x[:-1] or x for x in file(filename).readlines()]
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
    log.append('pid: '+str(os.getpid()))
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
