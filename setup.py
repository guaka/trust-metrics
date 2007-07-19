#!/usr/bin/env python

from distutils.core import setup
import trustlet


setup(	name = 'trustlet',
	version = trustlet.__version__,
	description = 'Analyse trust metrics on social networks',
	author = 'Kasper Souren, Paolo Massa and others',
	author_email = 'souren@itc.it',
	url = 'http://trustlet.org/wiki/Code',
	license = 'GPL',
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
	long_description = "\n".join(trustlet.__doc__.split('\n')),
	# py_modules = ['trustlet', 'pymmetry'],
        scripts=['scripts/dataset-downloader'],
        packages = ['trustlet', 'pymmetry']
        )
