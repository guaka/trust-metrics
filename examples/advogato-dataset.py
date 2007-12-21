"""
Load some datasets (possibly download them from the internet) and show
some information.
"""

# make sure example can be run from examples/ directory
import sys
sys.path.append('../trustlet')

from Advogato import *

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
