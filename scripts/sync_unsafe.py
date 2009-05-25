#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
this script syncronizes local datasets database with the remote database (on trustlet.org).
It uses svn.

First of all it'll download missed datasets.
Then merge them with the local version of them.
 - Only c2 file are mergerd. If a regular file yet exists on client it won't updated.
Finally *all* changes will be committed.
 - Backup files (ends with ~) will not uploaded.
 - Files and directory that begin with + will not uploaded too.

main directory dataset: <basepath>/datasets
svn hidden directory: <basepath>/.datasets

sync creates ~/datasets and ~/.datasets links

sync.py [basepath] [other options]

 - path can be a dir or a file

Options:
   --no-update:  no svn update. ¡¡¡ Dangerous option !!!
   --no-upload:  no upload generated files
   -c <comment>  add <comment> to commit comment
   --verbose | -v

Is *dangeous* executes sync while someone uses cache.
'''

import os
import os.path as path
import sys
import shutil
import re
import time
from socket import gethostname

# not show: /usr/lib/python2.6/site-packages/networkx/hybrid.py:16: DeprecationWarning: the sets module is deprecated
stderr = sys.stderr
sys.stderr = file('/dev/null','w')
from trustlet.helpers import merge_cache,mkpath,md5file,relative_path,safe_merge,read_c2
sys.stderr = stderr

HOME = os.environ['HOME']
HOSTNAME = gethostname()
PREFIX = '+'
CURDIR = os.getcwd()
HIDDENDIR = '.shared_datasets'
DIR = 'shared_datasets'
SVNCO = 'svn co --non-interactive http://www.trustlet.org/trustlet_dataset_svn "%s"'
SVNUP = 'svn up --non-interactive --username anybody --password a'
SVNCI = 'svn ci --non-interactive --username anybody --password a -m "automatic commit by %s (sync.py)%s"' % (HOSTNAME,'%s')
SVNADD = 'svn add "%s"'

REMOVED = 'removed'
MAX_SIZE_REMOVED = 20

CONFLICT =  '''You may resolve conflicts in %s dir svn.
Try svn update, and remove any conflict deleting local files.
Execute svn resolved <file> for each removed file.
Now svn commit doesn't upload anything and sync.py may work.
''' % path.join(os.environ['HOME'],HIDDENDIR)

size = lambda f: os.stat(f).st_size
mtime = lambda f: int(os.stat(f).st_mtime)
re_svnconflict = re.compile('.*\.r\d+$') #ends with .r[num]


def svnadd(p):
    assert not os.system(SVNADD % p),SVNADD % p

def svnaddpath(p):
    
    assert path.abspath(p)!=os.path.sep,p

    if path.isdir(path.join(p,'.svn')):
        return True
    
    if svnaddpath(path.join(p,os.pardir)):
        svnadd(p)

    return False

def main():

    if 'help' in sys.argv or '--help' in sys.argv:
        print __doc__
        return

    # set comment
    if '-c' in sys.argv[1:-1]:
        i = sys.argv.index('-c')
        usercomment = sys.argv[i+1]
        del sys.argv[i+1]
        del sys.argv[i]
    else:
        usercomment = ''

    if sys.argv[1:] and sys.argv[1][0]!='-':
        basepath = path.realpath(sys.argv[1])
    else:
        basepath = HOME

    hiddenpath = path.join(basepath,HIDDENDIR)
    datasetspath = path.join(basepath,DIR)

    #remove old links
    if path.islink(path.join(HOME,HIDDENDIR)):
        os.remove(path.join(HOME,HIDDENDIR))
    if path.islink(path.join(HOME,DIR)):
        os.remove(path.join(HOME,DIR))

    if basepath != HOME:
        path1 = path.join(HOME,HIDDENDIR)
        path2 = path.join(HOME,DIR)
        assert not path.islink(path1) and not path.exists(path1),'remove '+path1
        assert not path.islink(path2) and not path.exists(path2),'remove '+path2
        assert not os.system('ln -s "%s" "%s"' % (hiddenpath,path1))
        assert not os.system('ln -s "%s" "%s"' % (datasetspath,path2))

    sys.argv = set(sys.argv)

    if '--verbose' in sys.argv:
        sys.argv.add('-v')

    upload = not '--no-upload' in sys.argv
    
    #files updated from svn
    file_updated = set()

    #timestamp update
    ###tstampup = 0
    if not path.isdir(hiddenpath) or not path.isdir(path.join(hiddenpath,'.svn')):
        # dir checking
        os.chdir(HOME)
        if path.exists(hiddenpath):
            shutil.rmtree(hiddenpath)
        assert not os.system(SVNCO % hiddenpath)
    else:
        os.chdir(hiddenpath)
        
        # obsolete ---
        #for dirpath,dirs,files in os.walk(hiddenpath):
        #    if not '.svn' in dirpath:
        #        # foreach file saves relative path
        #        file_updated += [path.join(dirpath,x) for x in files]
        # ---

        #timestamp update ..> I can use ts of the last execution of sync?
        ###tstampup = int(time.time())
        lastupload = load_upload_timestamp()
        assert not os.system(SVNUP),'Update failied. '+CONFLICT

        #file_updated = set(file_updated)

        for dirpath,dirs,files in os.walk(hiddenpath):
            if not '.svn' in dirpath:
                # remove from file_updated files yet in datasets dir only if
                # they have not been modified.
                #unchanged = set([path.join(dirpath,x) for x in files
                #                 if mtime(path.join(dirpath,x))<tstampup])
                #file_updated.difference_update(unchanged)

                file_updated |= set([path.join(dirpath,x) for x in files
                                     if mtime(path.join(dirpath,x))>lastupload])

        added = updated = uploaded = merged = 0

        #print file_updated

        # update files modifiedy both from server and from client
        for p1 in file_updated:
            p2 = p1.replace(hiddenpath,datasetspath)

            if p1.endswith('.c2') and os.path.isfile(p2):
                # sure that p2 is updated
                safe_merge(p2)
                
            if p1.endswith('.c2') and mtime(p2)>lastupload:

                # modified from last time (both server and client) -> merge
                if merge_cache([p1,p2],p1):
                    shutil.copy(p1,p2)
                    print p1,DIR
                    print 'merged',relative_path(p1,DIR)[1]
                    merged += 1
            else:
                print p2,DIR
                print "I'm updating (coping)",relative_path(p2,DIR)[1] # ¡¡¡ it might a lost update, non c2 files only !!!
                shutil.copy(p1,p2) # hiddenpath -> datasetpath
                updated += 1


        # from svn to datasets
        for dirpath,dirnames,filenames in os.walk(hiddenpath):
            if '.svn' in dirpath:
                continue

            destbasepath = dirpath.replace(hiddenpath,datasetspath)

            # create missing directory
            if not path.isdir(destbasepath):
                os.mkdir(destbasepath)

            for filename in filenames:
                #print filename
                srcpath = path.join(dirpath,filename)
                dstpath = path.join(destbasepath,filename)
                # relative path, without HOME/(.)datasetspath
                rpath = relative_path(srcpath,HIDDENDIR)[1]
                #print '<<< File:',rpath

                if path.isfile(dstpath):

                    # Manage removed files
                    if removed(srcpath):
                        print 'I\'m removing',dstpath
                        os.remove(dstpath)
                        continue

                    if not srcpath in file_updated and mtime(dstpath)>lastupload:
                        #updated from client and not from server
                        print 'Upload',rpath
                        uploaded += 1
                        shutil.copy(dstpath,srcpath)

                elif filename[0]!=PREFIX and not re_svnconflict.match(filename) and not filename.endswith('.mine') and not removed(srcpath) and not filename.endswith('.lock'):
                    #adding
                    print 'adding file',rpath
                    added += 1
                    #print srcpath,dstpath
                    shutil.copy(srcpath,dstpath)

        if added:
            print '# of added files from server:',added
        if updated:
            print '# of updated files:',updated
        if uploaded:
            print '# of updated files:',uploaded
        if merged:
            print '# of merged files:',merged

        # from datasetspath to svn

        # to adding files
        os.chdir(hiddenpath)

        #copy *new* files to upload dir (hiddenpath)
        for dirpath,dirnames,filenames in os.walk(datasetspath):
            #print '>>',dirpath
            destbasepath = dirpath.replace(datasetspath,hiddenpath)

            if path.sep+PREFIX in dirpath:
                # not upload dirs +*
                print 'Directory %s will not uploaded' % path.split(dirpath)[1]
                continue

            # merge locally c2 files ( name.\d+.c2 into name.c2 )
            for filename in filenames:
                srcpath = path.join(dirpath,filename)
                dstpath = path.join(destbasepath,filename)
                
                # if dstpath in file_updated -» yet merged
                if srcpath.endswith('.c2') and path.exists(srcpath) and dstpath not in file_updated:
                    #print 'Merge:',srcpath
                    safe_merge(srcpath)

            for filename in filenames:

                srcpath = path.join(dirpath,filename)
                if not path.exists(srcpath):
                    continue #merging c2 might erase files
                dstpath = path.join(destbasepath,filename)
                # relative path, without HOME/(.)datasetspath
                rpath = relative_path(srcpath,DIR)[1]
                #print '>>> File:',rpath

                if filename.startswith(PREFIX) or re_svnconflict.match(filename) \
                        or filename.endswith('.mine') or filename.endswith('~') \
                        or filename.endswith('.lock'):
                    # not upload files _*, svn file and backup files
                    print 'File %s will not uploaded' % rpath
                    continue

                if not path.isfile(dstpath):
                    print 'adding file',rpath
                    added += 1

                    mkpath(destbasepath)
                    svnaddpath(destbasepath)
                    shutil.copy(srcpath,destbasepath)
                    svnadd(dstpath)
                #print  '<',srcpath,srcpath in updatedc2

        #print updatedc2

        comment = ''
        if added:
            comment += ' Added %d files.' % added
        if updated:
            comment += ' Updated %d files.' % uploaded

        if usercomment:
            comment += ' ' + usercomment

        if comment and '-v' in sys.argv:
            print 'Commit comment:', comment
        assert not os.system(SVNCI % comment),CONFLICT

        if added:
            print '# of added files to server repository:',added
    
    os.chdir(CURDIR)

    # this is the last thing to do because a crash after save_upload_ts()
    # without upload new data will cause a lost of them
    save_upload_timestamp()

def diff(f,g):
    '''
    return True if 2 files are equal
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

def diffc2(f,g):
    '''
    return True if 2 c2 files are equal
    '''
    if type(f) is str:
        f = read_c2(f)

    if type(g) is str:
        g = read_c2(g)

    assert type(f) is type(g) is dict,type(f)

    if set(f.keys()) != set(g.keys()):
        return False

    for k in f:
        if f[k]['ts'] != g[k]['ts']:
            return False

    return True

def removed(path):
    '''Manage removed files'''
    if size(path)<=MAX_SIZE_REMOVED:
        #print 'Small file'
        f = file(path)
        data = f.read().strip()
        f.close()
        
        if data==REMOVED:
            return True
        
    return False

def save_upload_timestamp():
    sut = file(os.path.join(HOME,'.syncuploadts'),'w')
    sut.write(str(time.time())+' '+time.ctime())
    sut.close()

def load_upload_timestamp():
    try:
        sut = file(os.path.join(HOME,'.syncuploadts'))
        data = float(sut.read().split()[0])
        sut.close()
        return data
    except IOError:
        return 0.

if __name__=="__main__":
    main()
