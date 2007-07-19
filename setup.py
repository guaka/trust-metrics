#!/usr/bin/env python

from distutils.core import setup
import pydot

setup(	name = 'trustlet',
	version = pydot.__version__,
	description = 'Analyse trust metrics on social networks',
	author = 'Kasper Souren',
	author_email = 'souren@itc.it',
	url = 'http://trustlet.org/wiki/Code',
	license = 'aGPLv3',
	platforms = ["any"],
	classifiers =	[
                   #     'Development Status :: 5 - Production/Stable',	\
                         'Intended Audience :: Science/Research',	\
                         'License :: OSI Approved :: GPL License',\
                         'Natural Language :: English',			\
                         'Operating System :: OS Independent',		\
                         'Programming Language :: Python',		\
                   #     'Topic :: Scientific/Engineering :: Visualization',\
                         'Topic :: Software Development :: Libraries :: Python Modules'],
	long_description = "\n".join(pydot.__doc__.split('\n')),
	# py_modules = ['trustlet', 'pymmetry']
        packages = ['trustlet', 'pymmetry']
        )
