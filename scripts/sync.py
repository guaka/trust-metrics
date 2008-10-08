#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Policy:
#

'''
this script syncronizes local datasets database with the remote database (on trustlet.org).
It uses svn.

First of all it'll download missed datasets.
Then merge them with the local version of them.
 - Only c2 file are mergerd. If a regular file yet exists on client it won't updated.
Finally changes will be committed.
 - Backup files (ends with ~) will not uploaded.

main directory dataset: ~/datasets
svn hidden directory: ~/.datasets

Parameters:
   --no-update: no svn update. ¡¡¡ Dangerous option !!!
   --no-upload: no upload generated files
   --verbose | -v
'''

import os
import sys
import shutil

from trustlet.helpers import merge_cache,mkpath

HOME = os.environ['HOME']
HIDDENPATH = os.path.join(HOME,'.datasets')
DATASETSPATH = os.path.join(HOME,'datasets')
CURDIR = os.getcwd()
SVNCO = 'svn co --non-interactive http://www.trustlet.org/trustlet_dataset_svn "%s"' % HIDDENPATH
SVNUP = 'svn up --username anybody --password a'
SVNCI = 'svn ci --username anybody --password a -m="auomatic commit (sync.py)"'
SVNADD = 'svn add "%s"'

def main():

    sys.argv = set(sys.argv)

    if 'help' in sys.argv:
        print __doc__
        return

    if '--verbose' in sys.argv:
        sys.argv.append('-v')

    if not os.path.isdir(HIDDENPATH) or not os.path.isdir(os.path.join(HIDDENPATH,'.svn')):
        os.chdir(HOME)
        assert not os.system(SVNCO)
    elif not '--no-update' in sys.argv:
        os.chdir(HIDDENPATH)
        assert not os.system(SVNUP)

    merge(HIDDENPATH,DATASETSPATH,not '--no-upload' in sys.argv)

    os.chdir(CURDIR)

def diff(f,g):
    '''
    return True if 2 file are equals
    '''
    if type(f) is str:
        f = file(f)
    if type(g) is str:
        g = file(g)

    while True:
        bf = f.read(512)
        bg = g.read(512)
        
        if bf != bg:
            f.close()
            g.close()
            return False
        if not bf:
            f.close()
            g.close()
            return True

def merge(svn,datasets,upload=True):
    added = updated = merged = 0
    updatedc2 = set()
    updatedfiles = set()
    # from svn to datasets
    for dirpath,dirnames,filenames in os.walk(svn):
        if '.svn' in dirpath:
            continue

        # workaround
        # Seems that in dirnames there are some filenames and viceversa.
        names = dirnames + filenames
        dirnames = [x for x in names if os.path.isdir(os.path.join(dirpath,x))]
        filenames = [x for x in names if os.path.isfile(os.path.join(dirpath,x))]
        #

        destbasepath = dirpath.replace(svn,datasets)
        
        if '-v' in sys.argv:
            print destbasepath
        if not os.path.isdir(destbasepath):
            assert not os.path.exists(destbasepath)
            os.mkdir(destbasepath)

        for filename in filenames:
            #print filename
            srcpath = os.path.join(dirpath,filename)
            dstpath = os.path.join(destbasepath,filename)
            
            if os.path.isfile(dstpath):
                if not diff(srcpath,dstpath):
                    # file modified
                    if filename.endswith('.c2'):
                        print 'merging file %s with new version' % filename
                        updatedc2.add(dstpath)
                        merged += 1
                        # priority: dstpath
                        merge_cache(srcpath,dstpath)
                    else:
                        print 'file %s differs from client to server. The client version will be kept.' % filename
                        updatedfiles.add(dstpath)
            else:
                #adding
                print 'adding file',filename
                added += 1
                print srcpath,dstpath
                shutil.copy(srcpath,dstpath)


    if added:
        print '# of added files:',added
    if updated:
        print '# of updated files:',updated
    if merged:
        print '# of merged files:',merged
    
    # from datasets to svn
    if upload:
        print 'Upload on server'
        added = 0

        # to adding files
        os.chdir(svn)

        #copy *new* files and updated c2 to upload dir (svn)
        for dirpath,dirnames,filenames in os.walk(datasets):
            destbasepath = dirpath.replace(datasets,svn)

            for filename in filenames:
                if filename.endswith('~'):
                    # skip backup files
                    continue

                srcpath = os.path.join(dirpath,filename)
                dstpath = os.path.join(destbasepath,filename)
            
                if not os.path.isfile(dstpath):
                    print 'adding file',filename
                    added += 1
                    mkpath(destbasepath, lambda x: os.system(SVNADD % x))
                    shutil.copy(srcpath,destbasepath)
                    assert not os.system(SVNADD % dstpath)
                elif srcpath in updatedc2:
                    print 'merging file',filename
                    shutil.copy(srcpath,dstpath)
                elif srcpath in updatedfiles:
                    print 'updating file',filename
                    shutil.copy(srcpath,dstpath)

        assert not os.system(SVNCI)

        if added:
            print '# of added files to server repository:',added
        

if __name__=="__main__":
    main()
