#!/usr/bin/env python
"""
test cache functions.
- save/load
- mmerge
"""

import unittest
import os
import sys
import random
import time

from trustlet import *

path = lambda x: '/tmp/testcache/%d.c2'%x

class TestCache(unittest.TestCase):
    
    def setUp(self):
        if os.path.exists('/tmp/testcache'):
            self.tearDown()
        os.mkdir('/tmp/testcache')
        
    def tearDown(self):
        assert 0==os.system('rm -rf /tmp/testcache')

    def test_store(self):

        NKEYS = 100
        data = set()
        p = path(0)

        # save
        for k in xrange(NKEYS):
            v = random.random()
            self.assert_(save(k,v,p))
            data.add((k,v))
        
        # load
        for k,v in data:
            self.assertEqual(load(k,p,cachedcache=True),load(k,p,cachedcache=False),v)


    #def test_cachedcache(self):
    #    pass

    def test_cachedcache(self):
        self.test_cache(True)

    def test_cache(self,cachedcache=False):
        '''
        test concurrency with cachedcache
        '''
        #syncronize
        r,w = os.pipe()
        rr,ww = os.pipe()

        N = 100
        p = path(0)
        k = ('K is The Key',ord('K'))

        def task(args):
            master,r,w = args
            if master:
                os.write(w,'.')

            # wrong data to confuse load with cachedcache
            for c in xrange(N):
                save(k+(c,),'>'*c,p)

            computed = set()

            self.assert_(os.read(r,1)=='.')

            for c in xrange(N):
                
                v = load(k+(c,),p,cachedcache=cachedcache)

                #print c
                if v != c:
                    self.assert_(save(k+(c,),c,p))
                    computed.add(c)
                    time.sleep(1.01)
                else:
                    continue
            
                #print master,'w'
                os.write(w,'.')
                #print master,'r'
                self.assert_(os.read(r,1)=='.')
                
            os.write(w,'.')

            return computed

        computed = splittask(task,[(1,r,ww),(0,rr,w)],showperc=False,notasksout=False)
        #print computed
        
        os.close(r)
        os.close(w)
        os.close(rr)
        os.close(ww)
        
        self.assertEquals(computed[0] & computed[1],set())
        self.assertEquals(len(computed[0] | computed[1]),N)

    def test_merge(self):

        NVALUES = 100
        NKEYS = 30
        NC2 = 10

        data = {}
        pp = set()

        for i in xrange(NVALUES):
            k = random.randint(0,NKEYS)
            v = random.random()
            p = path(random.randint(0,NC2))
            pp.add(p)
            #print k,v,p
            self.assert_(save(k,v,p))
            data[k] = v

        pp = list(pp)

        out = pp[random.randint(0,NC2)]

        merge_cache(pp,out)

        c2 = read_c2(out)

        for k,v in c2.iteritems():
            self.assert_(k in data)
            self.assertEqual(data[k],v['dt'])

if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCache)
    unittest.TextTestRunner(verbosity=2).run(suite)
