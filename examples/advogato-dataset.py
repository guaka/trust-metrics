"""
Load some datasets (possibly download them from the internet) and show
some information.
"""

# make sure example can be run from examples/ directory
import sys
sys.path.append('../trustlet')

from Dataset.Advogato import *
from Dataset.Dummy import DummyNetwork

# create dummy dataset
D = DummyNetwork()
D.info() # show information

# create Kaitiaki dataset
K = KaitiakiNetwork()
K.info() # show information

# create SqueakFoundation dataset
S = SqueakFoundationNetwork()
S.info()

# create Advogato dataset
A = AdvogatoNetwork()
A.info() 

# create Advogato dataset as it was on a certain date.
# The .dot file is taken from http://www.trustlet.org/datasets/advogato/ looking for the correctly dated file
AD = AdvogatoNetwork(2007,10,13)
AD.info() 

