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

    def splittask(self,np):
        
        input = range(40)
        self.assertEqual(splittask(lambda x:x,input,showperc=False,np=np),input)
    
    def test_splittask_1(self):
        self.splittask(1)
    def test_splittask_2(self):
        self.splittask(2)
    def test_splittask_3(self):
        self.splittask(3)
    def test_splittask_4(self):
        self.splittask(4)
    def test_splittask_5(self):
        self.splittask(5)
    def test_splittask_6(self):
        self.splittask(6)
    def test_splittask_7(self):
        self.splittask(7)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCache)
    unittest.TextTestRunner(verbosity=2).run(suite)
