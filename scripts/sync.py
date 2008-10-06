#!/usr/bin/env python    
# -*- indent-tabs-mode:nil; tab-width:4 -*-

'''
this script syncronize local datasets database with the remote database (on trustlet.org).
It uses svn.

First of all it'll download missed datasets.
Then merge them with the local version of them.
Finally changes will be committed.

main directory dataset: ~/datasets
svn hidden directory: ~/.datasets

Parameters:
   --no-update
   --no-upload
'''

import os
import sys
import shutil

from trustlet.helpers import merge_cache

HOME = os.environ['HOME']
HIDDENPATH = os.path.join(HOME,'.datasets')
DATASETSPATH = os.path.join(HOME,'datasets_temp')
CURDIR = os.getcwd()
SVNCO = 'svn co --non-interactive http://www.trustlet.org/trustlet_dataset_svn %s' % HIDDENPATH
SVNUP = 'svn up --username anybody --password a'
SVNCI = 'svn ci --username anybody --password a -m="auomatic commit"'
SVNADD = 'svn add %s'

def main():
    if not os.path.isdir(HIDDENPATH) or not os.path.isdir(os.path.join(HIDDENPATH,'.svn')):
        os.chdir(HOME)
        os.system(SVNCO)
    elif not '--no-update' in sys.argv:
        os.chdir(HIDDENPATH)
        os.system(SVNUP)

    merge(HIDDENPATH,DATASETSPATH,not '--no-upload' in sys.argv)

    os.chdir(CURDIR)

read = 0 # KB readed

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
        
        # KB readed from diff
        globals()['read'] += 1
        
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
    # from svn to datasets
    for dirpath,dirnames,filenames in os.walk(svn):
        if '.svn' in dirpath:
            continue
        destbasepath = dirpath.replace(svn,datasets)
        
        if not os.path.isdir(destbasepath):
            os.mkdir(destbasepath)

        for filename in filenames:
            srcpath = os.path.join(dirpath,filename)
            dstpath = os.path.join(destbasepath,filename)
            
            if os.path.isfile(dstpath):
                if not diff(srcpath,dstpath):
                    # file modified
                    if filename.endswith('.c2'):
                        print 'merging file %s with new version' % filename
                        merged += 1
                        merge_cache(srcpath,dstpath)
                    else:
                        #update
                        print 'updating file',filename
                        updated += 1
                        shutil.copy(srcpath,dstpath)
            else:
                #adding
                print 'adding file',filename
                added += 1
                shutil.copy(srcpath,dstpath)

    print added, updated, merged

    # from datasets to svn
    if upload:
        print 'Upload on server'
        added = updated = 0

        #copy modified file to upload dir (svn)
        for dirpath,dirnames,filenames in os.walk(datasets):
            destbasepath = dirpath.replace(datasets,svn)

            for filename in filenames:
                srcpath = os.path.join(dirpath,filename)
                dstpath = os.path.join(destbasepath,filename)
            
                if not os.path.isfile(dstpath):
                    print 'adding file',filename
                elif not diff(srcpath,dstpath):
                    print 'updated file',filename
                    updated += 1
                    shutil.copy(srcpath,dstpath)

        # adding new files to svn
        os.chdir(svn)
        for dirpath,dirnames,filenames in os.walk(svn):
            if not '.svn' in dirnames:
                print dirpath
                os.system(SVNADD % dirpath)

        print added, updated
        

if __name__=="__main__":
    main()
