"""
trustlet
========

   trustlet is a Python package for the study of trust metrics on
   social networks.  As of October 2007 it is in alpha stage, with
   support for several Advogato-like datasets and a bunch of trust
   metrics.

   http://trustlet.org/

Using 
-----

   >>> from trustlet import *
   >>> AD = AdvogatoNetwork(date="2007-10-13")
   >>> AD.info() 
... add more here
"""


# how to use subversion revision number?
__version__ = '0.1.2' # + "-r" + $Revision: $


from Dataset.Advogato import *
from Dataset.Dummy import *
from TrustMetric import *
from PredGraph import *
