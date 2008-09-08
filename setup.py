#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for networkx

"""

from glob import glob
import os
import sys
if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')

from distutils.core import setup
import trustlet

version = trustlet.__version__

if not 'install' in sys.argv[1:]:
    print "To install, run 'python setup.py install'"
    print

if sys.version_info[:2] < (2, 3):
    print "trustlet requires Python version 2.3 or later (%d.%d detected)." % \
          sys.version_info[:2]
    sys.exit(-1)


docdirbase  = 'share/doc/trustlet-%s' % version
data = [# (docdirbase, glob("doc/*.txt")),
        (os.path.join(docdirbase, 'examples'),glob("examples/*.py")),
        # (os.path.join(docdirbase, 'examples'),glob("doc/examples/*.dat")),
        # (os.path.join(docdirbase, 'examples'),glob("doc/examples/*.edges")),
        # (os.path.join(docdirbase, 'data'),glob("doc/data/*ls")),
        ]

package_data     = {'': ['*.txt'],} 


dependencies = ['igraph',
                'pygraphviz',
                'pyparsing',
                'networkx',
                'numpy',
                'scipy',
                'python-gnuplot'
                ]  

pkg = ['trustlet', 'trustlet.pymmetry', 'trustlet.Dataset']

setup(	name = 'trustlet',
	version = version,
	description = 'Analyse trust metrics on social networks',
	author = 'Kasper Souren, Paolo Massa and others',
	author_email = 'kasper.souren@gmail.com',
	url = 'http://trustlet.org/wiki/Code',
	license = 'GPL',
	platforms = ["any"],
        # see http://www.python.org/pypi?%3Aaction=list_classifiers
	classifiers = ['Development Status :: 2 - Pre-Alpha',
                       'Intended Audience :: Science/Research', 
                       'License :: OSI Approved :: GNU General Public License (GPL)', 
                       'Natural Language :: English',			
                       'Operating System :: Linux/OSX',		
                       'Programming Language :: Python',		
                       'Topic :: Scientific/Engineering :: Visualization',
                       'Topic :: Software Development :: Libraries :: Python Modules'
                       ],
	long_description = "\n".join(trustlet.__doc__.split('\n')),
	# py_modules = ['trustlet', 'pymmetry'],
        scripts = ['scripts/dataset-downloader'],
        packages = pkg,
        data_files = data,
        package_data = package_data,
        )
#copy datasets on home folder
#os.system( 'cp -Rf ./trustlet/datasets ~' )
if False:
    print "Installing scripts\n"
    os.system( 'cd trustlet && make install && cd ..' )
    os.system( 'cd scripts && make install && cd ..' )

print "Now we try to checkout all the datasets from www.trustlet.org This operation maybe longer."
print "If you have always the internet connection enabled, when the datasets were used"
print "they can be automatically downloaded from www.trustlet.org, and then you don't need"
print "to check out all of them now. But if you think to work on a isolate pc"
print "without an internet connection, is better to download all now."
print "RECCOMENDED: don't download now"
print "QUESTION: Do you want to download all the datasets now? [N,y]"
c = raw_input()
if 'y' in c:
    print "Wait this operation maybe longer... Try to download datasets"
    print "Important: Do not stop this"
    os.system( 'svn co --non-interactive http://www.trustlet.org/trustlet_dataset_svn trustlet/datasets' )
else:
    print "Wait a moment please.. Try to download datasets.."
    os.system( 'svn co --non-interactive http://www.trustlet.org/trustlet_dataset_svn trustlet/datasets -r 24' ) #19 and 2 is an empty revision

os.chdir( './trustlet' )
os.system( 'chmod -Rf 777 ./datasets' )
os.chdir( '..' )

print "IMPORTANT: remember to create a simbolic link to trustlet/datasets folder in your home directory!"
print "If you would partecipate in development of trustlet, and you"
print "wouldn't edit file in your installation dir, you can use links.py in scripts/ folder"
# It's not very clear how to deal with package dependencies in setup.py

#import pkg_resources
#pkg_resources.require(dependencies)
