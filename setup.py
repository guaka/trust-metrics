#!/usr/bin/env python

from distutils.core import setup
import trustlet


setup(	name = 'trustlet',
	version = trustlet.__version__,
	description = 'Analyse trust metrics on social networks',
	author = 'Kasper Souren, Paolo Massa and others',
	author_email = 'kasper.souren@gmail.com',
	url = 'http://trustlet.org/wiki/Code',
	license = 'GPL',
	platforms = ["any"],
        # see http://www.python.org/pypi?%3Aaction=list_classifiers
	classifiers =	['Development Status :: 2 - Pre-Alpha',	\
                         'Intended Audience :: Science/Research',	\
                         'License :: OSI Approved :: GNU General Public License (GPL)', \
                         'Natural Language :: English',			\
                         'Operating System :: OS Independent',		\
                         'Programming Language :: Python',		\
                         'Topic :: Scientific/Engineering :: Visualization',\
                         'Topic :: Software Development :: Libraries :: Python Modules'],
	long_description = "\n".join(trustlet.__doc__.split('\n')),
	# py_modules = ['trustlet', 'pymmetry'],
        scripts = ['scripts/dataset-downloader'],
        packages = ['trustlet', 'trustlet.pymmetry', 'trustlet.Dataset'],

        # this doesn't work really well with Python 2.5.1 and
        # setuptools 0.6c6 on guaka's RH machine called power at IRST
        install_requires = ['igraph',
                            'pyparsing',
                            'pygraphviz',
                            'numpy',
                            'networkx']  
        )
