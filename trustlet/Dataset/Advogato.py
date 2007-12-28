#!/usr/bin/env python
#
#
# trustlet is a project to analyze trust metrics on social networks.
#
#   Copyright (C) 2007  Kasper Souren <kasper.souren@gmail.com>, Paolo Massa <massa@itc.it>
#
#   This program is free software; you can redistribute it and/or modify
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

__author__ = """Kasper Souren (kasper.souren@gmail.com)\nPaolo Massa (massa@itc.it)"""
__license__ = "GPL"

from Network import WeightedNetwork
import os
import re
import datetime



_color_map = {
    'violet': 1.0, #master
    'blue': 0.8,   #journeyer
    'green': 0.6,  #apprentice
    'gray': 0.4,   #observer
    }


_obs_app_jour_mas_map = {
    'Observer': 0.4,
    'Apprentice': 0.6,
    'Journeyer': 0.8,
    'Master': 1.0
    }


class AdvogatoNetwork(WeightedNetwork):
    """The Advogato dataset.

http://www.trustlet.org/datasets/advogato/advogato-graph-2007-10-13.dot
"""
    orig_url = "http://www.advogato.org/person/graph.dot"
    dotfile = 'graph.dot'

    # seeds for global advogato TM
    advogato_seeds = ['raph', 'federico', 'miguel', 'alan']

    def __init__(self, date = None, comp_threshold = 0):
        """e.g. A = Advogato(date = '2007-12-21')"""

        self.url = ('http://www.trustlet.org/datasets/' +
                    self._name_lowered() + '/' +
                    self._name_lowered())
        if not date:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            self.url += '-graph-latest.dot'
        else:
            self.url += '-graph-' + date + '.dot'
        self.date = date

        # until 2006-05-20 there were colors on the edges
        if date <= "2006-05-20":
            self.level_map = _color_map
        else:
            self.level_map = _obs_app_jour_mas_map

        WeightedNetwork.__init__(self, weights = self.level_map)

        self.path = os.path.join(self.path, date)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.filepath = os.path.join(self.path, self.dotfile)
        self.download(only_if_needed = True)
        self.get_graph_dot()

        # DEPRECATED?
        if comp_threshold:
            self.ditch_components(comp_threshold)

    def _name_lowered(self):
        """Helper for url."""
        name = self.__class__.__name__.lower()
        if name[-7:] == 'network':
            name = name[:-7]
        return name


    def trust_on_edge(self, edge):
        """Trust level on edge."""
        return self.level_map[edge[2].values()[0]]  # ['level']]

    def info(self):
        WeightedNetwork.info(self)
        print "Level distribution:"
        for l in self.level_distribution():
            print l

    def level_distribution(self):
        return map(lambda s: (s, len([e
                                      for e in self.edges_iter()
                                      if e[2].values()[0] == s])), self.level_map.keys())
        

    def download(self, only_if_needed = False):
        """Download dataset."""
        if only_if_needed and os.path.exists(self.filepath):
            return
        self.download_file(self.url, self.dotfile)
        self.fix_graphdot()

    def fix_graphdot(self):
        """Fix syntax of graph.dot (8bit -> blah doesn't work!)"""
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

    def get_graph_dot(self, filepath = None):
        """Read graph.dot file into object."""
        if not filepath:
            filepath = self.filepath
        self._read_dot(filepath)


class RobotsNetNetwork(AdvogatoNetwork):
    """
    See http://trustlet.org/wiki/Robots.net
    Problem: spaces in graph.dot
    """
    url = "http://robots.net/person/graph.dot"

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

class SqueakFoundationNetwork(AdvogatoNetwork):
    """Squeak Foundation dataset"""
    url = "http://people.squeakfoundation.org/person/graph.dot"
    level_map = {
        'violet': 1.0, #master
        'blue': 0.8,   #journeyer
        'green': 0.6,  #apprentice
        'gray': 0.4,   #observer
        }

    # seeds for global advogato TM
    advogato_seeds = ['Yoda', 'luciano']
    def trust_on_edge(self, edge):
        """For Squeak it's color."""
        # print "in trust_on_edge, edge:", edge
        # x = edge[2]
        return self.level_map[edge[2]['color']]


class KaitiakiNetwork(SqueakFoundationNetwork):
    """Kaitaki dataset"""
    url = "http://www.kaitiaki.org.nz/virgule/person/graph.dot"
    advogato_seeds = ['susan', 'lucyt']



if __name__ == "__main__":
    S = SqueakFoundationNetwork(date = '2007-12-20')
    
    
