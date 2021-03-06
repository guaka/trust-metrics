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

import re

__version__ = '0.2' #+ '-r' + re.match('\$'+'Rev: (\d*) \$','$Rev: 1312 $').group(1) # doesn't work -_-

#import igraphXdigraphMatch
from Dataset.Network import *
from Dataset.Dummy import *
from Dataset.Advogato import *
from TrustMetric import *
from PredGraph import *
from netevolution import *
from conversion import *
#from igraphXdigraphMatch import *

#should come last since it overrides some networkx functions
from conv import * 
