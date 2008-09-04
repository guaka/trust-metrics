"""
Load some datasets (possibly download them from the internet) and show
some information.
"""

from trustlet import *

# create dummy dataset
D = DummyNetwork()
D.info() # show information

# create Kaitiaki dataset
K = KaitiakiNetwork(download = True, date='2008-09-01')
K.info() # show information

# create SqueakFoundation dataset
S = SqueakFoundationNetwork(download=True)
S.info()

# create Advogato dataset
A = AdvogatoNetwork(download=True)
A.info() 

# create Advogato dataset as it was on a certain date.
# The .dot file is taken from http://www.trustlet.org/datasets/advogato/ looking for the correctly dated file


AD = AdvogatoNetwork(date="2007-10-13", download=True)
AD.info() 

# create Advogato dataset as it was on a certain date.
# The .dot file is taken from http://www.trustlet.org/datasets/advogato/ looking for the correctly dated file

AOD = AdvogatoNetwork(date="2004-10-28",download=True) # the format of this file is with "violet, green, blue" on the edges and it is different from the current one with "journeyer, master, ..."
AOD.info()

