#!/usr/bin/env python
"""
test cache functions.
- save/load
- mmerge
"""

import unittest
#import os
#import sys
#import random
#import time

from trustlet import *

path = lambda x: '/tmp/testcache/%d.c2'%x

class TestCache(unittest.TestCase):

    def test_splittask(self):
        
        input = range(10)

        for np in xrange(1,7):
            self.assertEqual(splittask(lambda x:x,input,showperc=False,np=np),input)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCache)
    unittest.TextTestRunner(verbosity=2).run(suite)
