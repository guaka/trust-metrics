#!/usr/bin/env python
#
#
# trustlet is a project to analyze trust metrics on social networks.
#
#   Copyright (C) 2007  Kasper Souren <kasper.souren@gmail.com>, Paolo Massa <massa@itc.it>
#
#   This program is free software; you can redsistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA



"""
This is a module implementing the Advogato datasets.


There are other communities which use the same advogato software
(mod_virgule) and so they have the same trust levels and system and
publish the trust graph.  We created classes for some of them here,
such as Kaitiaki and SqueakFoundation.

More to add:
 * persone.softwarelibero.org  
      Paolo can probably easily obtain the dataset that is not
      downloadable at the standard person/graph.dot location)

"""

__author__ = """Kasper Souren (kasper.souren@gmail.com)
Paolo Massa (massa@itc.it)
Danilo Tomasoni (ciropom@gmail.com)
Martino Salvetti (martino@silix.org)"""
__license__ = "GPL"

import trustlet
import os
import re
import datetime


_color_map = {
    'violet': 1.0, #master
    'blue': 0.8,   #journeyer
    'green': 0.6,  #apprentice
    'gray': 0.4,   #observer
    '' : 0.0,
    # Workaround !!!
    'Observer': 0.4,
    'Apprentice': 0.6,
    'Journeyer': 0.8,
    'Master': 1.0,
    }


_obs_app_jour_mas_map = {
    'Observer': 0.4,
    'Apprentice': 0.6,
    'Journeyer': 0.8,
    'Master': 1.0,
    '' : 0.0
    }


class AdvogatoNetwork(trustlet.Dataset.Network.WeightedNetwork):
    """The Advogato dataset.

    http://www.trustlet.org/datasets/advogato/advogato-graph-2007-10-13.dot
    
    NB: if you would know what kind of network are hosted on www.trustlet.org invoke getNetworkList() from trustlet.helpers
    """
    orig_url = "http://www.advogato.org/person/graph.dot"
    dotfile = 'graph.dot'

    # seeds for global advogato TM
    advogato_seeds = ['raph', 'federico', 'miguel', 'alan']

    def __init__(self, date = None, weights = _obs_app_jour_mas_map, comp_threshold = 0, download = False, base_path = '',prefix=None):

        """
        e.g. A = Advogato(date = '2007-12-21')
        date = the date of the dot file, if you would to use a old dataset
        base_path=the path in wich is located the datasets folder
        weights = if no value is assigned to this parameter, the class choose automatically
        between _color_map and _obs_app_jour_mas_map
        comp_threshold = if this parameter is set, the class evaluate the ditch component
        """

        self.url = ('http://www.trustlet.org/datasets/' +
                    self._name_lowered() + '/' +
                    self._name_lowered())
        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            self.url += '-graph-latest.dot'
        else:
            self.url += '-graph-' + date + '.dot'
        self.date = date

        # it isn't true.. there are only observer etc.
        #if not weights:
            # until 2006-05-20 there were colors on the edges
            
        if date <= "2006-05-20":
            weights = _color_map
            self.key_on_edge = 'color'
        else:
            self.key_on_edge = 'level'
           #weights = _obs_app_jour_mas_map

        self.level_map = weights #level_map deprecated
        trustlet.Dataset.Network.WeightedNetwork.__init__(self, weights = self.level_map, base_path = base_path,prefix=prefix)

        self.path = os.path.join(self.path, date)
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self.c2file = self.dotfile[:-3]+"c2"

        self.filepath = os.path.join(self.path, self.c2file)
        self.dotpath = self.filepath[:-2]+'dot'
        
        #'download' parameter say to the class if download the source dot file or not
        self.download(only_if_needed = download)
        self.get_graph()

        # DEPRECATED?
        if comp_threshold:
            self.ditch_components(comp_threshold)

    def _name_lowered(self):
        """Helper for url."""
        name = self.__class__.__name__.lower()
        if name[-7:] == 'network':
            name = name[:-7]
        return name

    def _name(self):
        """
        return Advogato, or Squeakfoundation, or Kaitiaki..
        """
        name = self._name_lowered()
        return name[0].upper()+name[1:] #up only first letter

    def trust_on_edge(self, edge):
        """Trust level on edge."""
        return self.level_map[edge[2].values()[0]]  # ['level']]

    def info(self):
        trustlet.Dataset.Network.WeightedNetwork.info(self)
        self.show_reciprocity_matrix()
        print "Level distribution:"
        for l in self.level_distribution():
            print l

    def level_distribution(self):
        return filter(lambda x:x[0],map(lambda s: (s, len([e for e in self.edges_iter()
                                      if e[2].values()[0] == s])), self.level_map.keys()))
        

    def __convert(self):
        """
        this function assume that self.filepath was set
        """
        print "dot format detected, converting dot file in c2..."
        
        #convert dot in c2
        if not trustlet.conversion.dot.to_c2(self.dotpath,self.filepath,{'network':self._name(),'date':self.date}):
            print "Error converting dot into c2 file."
            return None
        #delete dot
        #os.remove( self.dotpath )
        
        print "Done."
        return None

    def download(self, only_if_needed = False):
        """Download dataset."""
        if os.path.exists(self.filepath):
            return

        if os.path.exists(self.dotpath):
            self.__convert()
            return

        if not os.path.exists(self.dotpath+'.bz2') and not only_if_needed:
            raise IOError("dot file does not exist (%s), if you would download it,\n"
                          "set 'download' parameter to True" % self.dotpath)
        else:
            if only_if_needed and (not os.path.exists(self.filepath)):
                self.download_file(self.url, self.dotfile)
                self.fix_graphdot()
                self.__convert()
                    

    def fix_graphdot(self):
        """
        Fix syntax of graph.dot (8bit -> blah doesn't work!)
        Put nodes names into `"`
        """
        print 'Fixing graph.dot'
        graph_file = open(self.filepath, 'r')
        l_names = graph_file.readlines()
        graph_file.close()
        re_fix = re.compile(' (\w+)')
        fixed_lines = map(lambda s: re_fix.sub(r' "\1"', s), l_names)

        writefile = open(self.filepath, 'w')
        writefile.writelines(fixed_lines)
        writefile.close()
        return self.filepath

    def get_graph(self, filepath = None):
        """Read graph.dot file into object."""
        if not filepath:
            filepath = self.filepath

        #self._read_dot(filepath)

        key = {'network':self._name(),'date':self.date}
        
        print "Reading ", filepath
        
        if not self.load_c2(key,self.key_on_edge): #if I can't be able to read
            raise IOError( "Error while loading network! the c2 doesn't exist in path "+self.filepath+" or does not contain this key "+str(key)  )
            

class Robots_netNetwork(AdvogatoNetwork):
    """
    See http://trustlet.org/wiki/Robots.net
    Problem: spaces in graph.dot
    """
    url = "http://robots.net/person/graph.dot"

    def __init__(self, date = None, weights = _obs_app_jour_mas_map, comp_threshold = 0, download = False, base_path = '',prefix=None):
        
        """
        e.g. A = Advogato(date = '2007-12-21')
        date = the date of the dot file, if you would to use a old dataset
        base_path=the path in wich is located the datasets folder
        weights = if no value is assigned to this parameter, the class choose automatically
        between _color_map and _obs_app_jour_mas_map
        comp_threshold = if this parameter is set, the class evaluate the ditch component
        """

        self.url = ('http://www.trustlet.org/datasets/' +
                    self._name_lowered() + '/' +
                    self._name_lowered())

        
        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            self.url += '-graph-latest.dot'
        else:
            self.url += '-graph-' + date + '.dot'
        self.date = date

        # it isn't true.. there are only observer etc.
        #if not weights:
            # until 2006-05-20 there were colors on the edges
            
        if date <= "2006-05-20":
            weights = _color_map
            self.key_on_edge = 'level'
        else:
            self.key_on_edge = 'color'
   
        self.level_map = weights #level_map deprecated
        trustlet.Dataset.Network.WeightedNetwork.__init__(self, weights = self.level_map, base_path = base_path,prefix=prefix)

        self.path = os.path.join(self.path, date)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.dotpath = os.path.join(self.path, self.dotfile)
        self.filepath = self.dotpath[:-3]+'c2'
        #'download' parameter say to the class if download the source dot file or not
        self.download(only_if_needed = download)
        self.get_graph()
            
        # DEPRECATED?
        if comp_threshold:
            self.ditch_components(comp_threshold)


    def fix_graphdot(self):
        """Fix syntax of graph.dot (8bit -> blah doesn't work!)"""
        print 'Fixing graph.dot'
        
        l_names = open(self.filepath, 'r').readlines()
        re_space = re.compile('(\w) (\w)')
        l_names_spacefix = map(lambda s:
                               re_space.sub(r'\1___\2', s).replace(".", "dot"),
                               l_names)

        pfix = re.compile(' ([\w\-_]+)')
        fixed_lines = map(lambda s: pfix.sub(r' "\1"', s), l_names_spacefix)
        import pprint
        pprint.pprint (fixed_lines)

        open(self.filepath + 'test', 'w').writelines(fixed_lines)
        return self.filepath + 'test'

class SqueakfoundationNetwork(AdvogatoNetwork):
    """Squeak Foundation dataset"""
    url = "http://people.squeakfoundation.org/person/graph.dot"

    def __init__(self, download = False, date=None, base_path=None,prefix=None):
        AdvogatoNetwork.__init__(self, weights = _color_map, download = download, date=date, base_path=base_path,prefix=prefix)

    # seeds for global advogato TM
    advogato_seeds = ['Yoda', 'luciano']
    def trust_on_edge(self, edge):
        """For Squeak it's color."""
        # print "in trust_on_edge, edge:", edge
        # x = edge[2]
        return self.level_map[edge[2]['color']]


class KaitiakiNetwork(SqueakfoundationNetwork):
    """Kaitaki dataset"""
    url = "http://www.kaitiaki.org.nz/virgule/person/graph.dot"
    advogato_seeds = ['susan', 'lucyt']

    def __init__(self, download=False, date = None, base_path = None,prefix=None):
        AdvogatoNetwork.__init__(self, weights = _color_map, download = download, date = date, base_path = base_path,prefix=prefix )


if __name__ == "__main__":
    S = SqueakfoundationNetwork(date = '2007-12-20')
    
    
