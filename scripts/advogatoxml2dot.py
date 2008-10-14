#!/usr/bin/env python

'''\
translation of old datasets in from xml to dot.
new datasets *don't* use this format.
'''

import os,re,sys
from os.path import join,isdir,isfile,exists
from trustlet import Network,helpers
from networkx import write_dot
from xml.dom.minidom import parse

if '--help' in sys.argv[1:] or len(sys.argv) < 2:
    print "USAGE: xml2dot [path]"
    sys.exit(1)

path = sys.argv[1]

addsep = lambda x: x[:4]+'-'+x[4:6]+'-'+x[6:8]

arcs = [x for x in os.listdir(path) if isfile(join(path,x)) and x[-8:]=='.tar.bz2']

os.chdir(path)
for arc in arcs:
    print 'Extracting',arc
    dir = arc[9:17]
    if exists(dir):
        print arc,"skipped"
        continue
    os.mkdir(dir)
    os.chdir(dir)
    os.system('tar xjf ../'+arc)
    os.chdir('..')

datasets = [x for x in os.listdir(path) if isdir(join(path,x))]

for dataset in datasets:
    datasetpath = join(path,dataset) + '/www.advogato.org/acct'
    userpath = datasetpath + "/%s/profile.xml"
    users = [x for x in os.listdir(datasetpath) if isdir(join(datasetpath,x))]
    
    n = Network.Network()
    for user in users:
        n.add_node(user)
        #print user

    for user in users:
        if not exists(userpath%user):
            print "Doesn't exist profile of "+user
            print userpath%user
            continue
        
        profile = parse(userpath%user)

        try:
            certs = profile.getElementsByTagName('certs')[0]
        except IndexError:
            # no votes
            continue

        #print "len(certs)",len(certs.getElementsByTagName('cert'))

        for cert in certs.getElementsByTagName('cert'):
            subj = str(cert.getAttribute('subj'))
            level = str(cert.getAttribute('level'))
            #print ">",user, subj, level
            n.add_edge(user,subj,{'value':level})
            
    os.mkdir(addsep(dataset))
    write_dot(n,join(path,addsep(dataset))+'/graph.dot')
