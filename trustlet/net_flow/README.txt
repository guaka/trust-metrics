from:   http://darcs.idyll.org/~t/projects/net_flow/README.html

net_flow
========

This is a Python wrapper around Raph Levien's "network flow"
implementation of a trust network.  See

        http://www.advogato.org/trust-metric.html

for more information.  It also contains a Python rewrite of the actual
trust metric used to calculate the advogato certifications, taken from
mod_virgule's 'tmetric.c' file.

You will need GLib version 2.0 installed in order to to compile
'net_flow.cc'.  See 'setup.py' for more information.

======

To build: 'python setup.py build'

To try it out after a 'python setup.py build',

   * make sure that your build/lib* directory is in your PYTHONPATH.

   * execute 'python examples/simple-network.py'

   * execute 'python examples/calc-advogato.py data/advogato.org-certs.txt \
	data/advogato.org-actual.txt'

For answers or random information on the python stuff, contact
Titus Brown <titus@caltech.edu>, or check out his advogato diary at

    http://www.advogato.org/person/titus/

=======

FILES::

   setup.py -- Python install script

   lib/net_flow.cc -- net_flow.c from mod_virgule project
   lib/net_flow.hh -- net_flow.h from mod_virgule project 
   lib/_net_flowmodule.cc -- Python wrapper for net_flow code.

   lib/net_flow.py -- class wrapper for _net_flow module.
   lib/advogato.py -- Python implementation of the advogato trust metric.

   examples/simple-network.py -- a simple network example
   examples/calc-advogato.py -- Calculation of the advogato trust certs.

   data/advogato.org-certs.txt -- certification network for www.advogato.org
   data/advogato.org-actual.txt -- actual cert levels for www.advogato.org

   data/robots.net-certs.txt -- certification network for www.robots.net
   data/robots.net-actual.txt -- actual cert levels for www.advogato.org



ABOUT THE LICENSE

There is no mention of the GPL. But net_flow.cc is from the Advogato
project, which is licensed under the GPL. So this net_flow-latest
wrapper must be available under the GNU General Public License as
well.

-- Kasper Souren, August 27, 2007.
