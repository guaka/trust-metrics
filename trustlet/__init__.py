"""
trustlet
========

   trustlet is a Python package for the study of trust metrics on
   social networks.  As of October 2007 it is in alpha stage, with
   support for several advogato-type datasets and a bunch of trust
   metrics.

   http://trustlet/

Using 
-----

   Just write in Python

   >>> from trustlet import *
   >>> G=Advogato()
   >>> G.add_edge(1,2)
   >>> G.add_node("spam")
   >>> print G.nodes()
   [1, 2, 'spam']
   >>> print G.edges()
   [(1, 2)]
"""


__version__ = '0.1.0'


from Advogato import *
from TrustMetric import *
from PredGraph import *
