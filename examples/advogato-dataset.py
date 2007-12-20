"""
Load some datasets (possibly download them from the internet) and show
some information.
"""

# make sure example can be run from examples/ directory
import sys
sys.path.append('../trustlet')



import Advogato

# create Kaitiaki dataset
K = Advogato.Kaitiaki()
K.info() # show information

# create SqueakFoundation dataset
S = Advogato.SqueakFoundation()
S.info()

# create Advogato dataset
A = Advogato.Advogato()
A.info() 
