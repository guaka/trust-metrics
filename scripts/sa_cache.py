
# == cache ==
# save and restore data into/from cache
# - `key` is a dictionary
# - `data` can be anything (i hope)

import os
import time
import cPickle as pickle
from gzip import GzipFile
from hashlib import md5

def mkpath(fullpath,function=None):
    """
    makes all missed directory of a path

    def function(path)
    function will called for each created dir.
    path is the path of it.
    """
    if not fullpath: return
    if fullpath[-1] == os.path.sep:
        fullpath = fullpath[:-1]
    if fullpath and not os.path.exists(fullpath):
        assert not os.path.islink(fullpath),'link %s might be broken' % fullpath
        path = os.path.split(fullpath)[0]
        mkpath(path)

        os.mkdir(fullpath)
        if function:
            function(fullpath)


def get_sign(key,mdfive=True):
    """
    Cache.
    Generate an unique key given a dictionary.
    If mdfive is True it will return an alphanumeric
    key of 32 chars
    """

    if not type(key) is dict:
        raise ValueError,'key have to be a dict'
    s = ''
    listkeys = key.keys()
    listkeys.sort()
    for k in listkeys:
        s+=str(k)+'='+str(key[k])+','
    if mdfive:
        return md5(s[:-1]).hexdigest()
    else:
        return s[:-1]

def hashable(x):
    """
    Cache.
    Return an hashable object that can be used as key in dictionary cache.
    """
    if type(x) in (str,tuple,frozenset,int,float):
        return x
    if type(x) is list:
        return (list,)+tuple(x)
    if type(x) is set:
        return frozenset(x)
    if type(x) is dict:
        tupleslist = []
        for k,v in x.iteritems():
            tupleslist.append( (k,v) )
        return frozenset(tupleslist)

    raise TypeError,"I don't know this type"

def save(key,data,path='.',human=False,version=3,threadsafe=True):
    """
    Cache.
    It stores some *data*  identified by *key* into a file in *path*.
    If human=True it will save another file in plain text for human beings.
    DEPRECATED: You can set *time* (integer, in seconds) to indicate the
    time of computation.
    If path ends with '.c2' (cache version 2) 
    data will save in the new format (less files).
    human is not suported in the new format.
    return: true in case of success, false in other cases
    """

    #debug
    #file(path+'.debug','w').write(str(data))

    # used by safe_save because it implements this
    if threadsafe:
        def lock():
            TIMEOUT = 300 # 5min
            def readall(fname):
                try:
                    f = file(fname)
                    data = f.read()
                    f.close()
                except:
                    data = ''
                return data or '0.0'
            def writeall(fname,data):
                f = file(fname,'w')
                f.write(data)
                f.close()
            while True:
                if not os.path.isfile(path+'.lock') or time.time()-float(readall(path+'.lock'))>TIMEOUT:
                    writeall(path+'.lock',str(time.time()))
                    return

                time.sleep(1)

        def unlock():
            try:
                os.remove(path+'.lock')
            except OSError:
                pass
    else:
        def lock():
            pass
        def unlock():
            pass

    if path.endswith('.c2'):
        mkpath(os.path.split(path)[0])
        lock()
        try:
            # I can't use cachedcache because data might be obsolete.
            d = pickle.load(GzipFile(path))
        except:
            d = {}
        #new version
        if version==3:
            # yet beta
            gen_key = hashable
        else:
            gen_key = get_sign

        d[gen_key(key)] = data
        ###
        #debug = file('debug')
        ###
        pickle.dump(d,GzipFile(path,'w'))
        unlock()

        #memory cache
        if not globals().has_key('cachedcache'):
            #print 'create cache'
            globals()['cachedcache'] = {}
        cache = globals()['cachedcache']
        cache[path] = d
    else:
        #version 1
        print "WARNING: don't use this cache version!"
        print "Add .c2 in path"
        mkpath(path)
        try:
            if human:
                f = file(os.path.join(path,get_sign(key,False)),'w')
                f.writelines([str(x)[:100]+'='+str(key[x])[:100]+'\n' for x in key])
                if type(human) is str:
                    f.write('comment: '+human)
                f.write('data: '+str(data))

            f = file(os.path.join(path,get_sign(key)),'w')
            pickle.dump(data,f)
            f.close()
        except IOError,pickle.PicklingError: #,TypeError: # I' can't catch TypeError O.o why?
            print 'picking error'
            return False
    return True
    
def safe_save(key,data,path):
    '''
    safe_save() is thread-safe version of save()
    Only version 3 is supported.
    '''
    
    assert path.endswith('.c2'),'Path doesn\'t ends with .c2'
    
    path = path[:-2] + str(os.getpid()) + '.c2'
    
    return save(key,data,path,threadsafe=False)

def safe_merge(path,delete=True):
    '''
    merge files created by safe_save into the original c2 (path)
    '''

    assert path.endswith('.c2'),'Path doesn\'t ends with .c2'

    fullpath = path
    path,name = os.path.split(fullpath)
    if not path:
        path = os.curdir

    #             get name.                   get pid.c2
    f = lambda x: x.startswith(name[:-2]) and repid.match(x[len(name)-2:])

    files = filter(f,os.listdir(path))

    for file in files:
        file = os.path.join(path,file)
        merge_cache(file,fullpath,ignoreerrors=True,priority=1)
        if delete:
            os.remove(file)

def load(key,path='.',fault=None):
    """
    Cache.
    Loads data stored by save.
    fault is the value returned if key is not stored in cache.
    """

    if os.path.isdir(path):
        try:
            data = pickle.load(file(os.path.join(path,get_sign(key))))
        except:
            return fault
    elif os.path.isfile(path):
        #memory cache
        if not globals().has_key('cachedcache'):
            #print 'create cache'
            globals()['cachedcache'] = {}
        cache = globals()['cachedcache']

        if cache.has_key(path):
            #print 'found',path
            try:
                if cache[path].has_key(get_sign(key)):
                    #version 2
                    return cache[path][get_sign(key)]
            except ValueError:
                pass
            if cache[path].has_key(hashable(key)):
                #version 3
                return cache[path][hashable(key)]
        try:
            d = pickle.load(GzipFile(path))
        except:
            return fault
        
        if d.has_key(hashable(key)):
            #version 3
            data = d[hashable(key)]
        elif d.has_key(get_sign(key)):
            #version 2
            data = d[get_sign(key)]
        else:
            return fault

        #save in memory cache
        cache[path] = d
    else:
        return fault

    return data

def erase_cachedcache():
    '''
    useful to reload cache from disc
    * doesn't work *
    '''
    globals()['cachedcache'] = {}

def convert_cache(path1,path2):
    '''
    from version 1 to 2
    * this function doesn't work *
    '''
    join = os.path.join
    oldcache = [(x,pickle.load(file(join(path1,x)))) \
                    for x in os.listdir(path1) if ismd5(x) and os.path.isfile(join(path1,x))]
    newcache = {}
    for k,v in oldcache:
        newcache[k] = v
    pickle.dump(newcache,GzipFile(path2,'w'))

def merge_cache(path1 , path2 , mpath=None, ignoreerrors=False, priority=2):
    '''
    mpath: new destination file (merged path).
    if mpath is None, *path2* will be used
    if `path1` and `path2` file cache has the same
    key will keep the `path2` value for that key.
    (To give priority to path1 set priority to 1)
    '''

    try:
        f1 = GzipFile(path1)
        c1 = pickle.load(f1)
        f1.close()
    except IOError:
        if ignoreerrors:
            c1 = {}
        else:
            print 'File %s corrupted' % path1
            return
    
    
    try:
        f2 = GzipFile(path2)
        c2 = pickle.load(f2)
        f2.close()
    except IOError:
        if ignoreerrors:
            c2 = {}
        else:
            print 'File %s corrupted' % path2
            return
    

    # Priority: c2
    # if c1 and c2 has the same key will keep the c2
    # value for that key
    if priority==2:
        c1.update(c2)
    elif priority==1:
        c2.update(c1)
        c1 = c2

    if not mpath:
        mpath = path2
    
    f = GzipFile(mpath ,'w')
    pickle.dump(c1,f)
    f.close()


def read_c2(path):
    '''return all cache dictionary'''
    return pickle.load(GzipFile(path))
