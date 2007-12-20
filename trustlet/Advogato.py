#!/usr/bin/env python

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

from Dataset.Network import WeightedNetwork
import os
import re

class Advogato(WeightedNetwork):
    """The Advogato dataset."""

    # TODO:
    #   * maybe change the name into Advogato_dataset?
    #
    #   * read files with a date as well (AdvogatoPast is an attempt
    #   to do this but maybe there is another way).  For example, in
    #   future we might want to store daily a copy of advogato
    #   graph.dot and save it on
    #   http://trustlet.org/datasets/advogato/ ) as graph20071012.dot
    #   (for now some files taken from archive.org are in
    #   http://phauly.bzaar.net/advogato_files/ )
    
    url = "http://www.advogato.org/person/graph.dot"
    dotfile = 'graph.dot'

    level_map = {
        'Observer': 0.4,
        'Apprentice': 0.6,
        'Journeyer': 0.8,
        'Master': 1.0
        }

    # seeds for global advogato TM
    advogato_seeds = ['raph', 'federico', 'miguel', 'alan']

    def __init__(self, filename = None, comp_threshold = 0):
        WeightedNetwork.__init__(self, weights = self.level_map)
        self.filepath = os.path.join(self.path, self.dotfile)
        self.download(only_if_needed = True)

        # ugly, temp workaround: RobotsNet isn't parsing properly yet
        if (self.__class__.__name__ == "RobotsNet"):
            self.fix_graphdot()

        if filename == "tiny":
            self.get_graph_dot("tiny_graph.dot")
        elif filename and os.path.exists(filename):
            self.get_graph_dot(filename)
        elif filename is None:
            self.get_graph_dot()

        if comp_threshold:
            self.ditch_components(comp_threshold)

    def trust_on_edge(self, edge):
        """Trust level on edge."""
        return self.level_map[edge[2]['level']]

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


class RobotsNet(Advogato):
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

class SqueakFoundation(Advogato):
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


class Kaitiaki(SqueakFoundation):
    """Kaitaki dataset"""
    url = "http://www.kaitiaki.org.nz/virgule/person/graph.dot"
    advogato_seeds = ['susan', 'lucyt']


class AdvogatoPast(Advogato):
    def __init__(self, date):
        raise NotImplemented

"""
        http://phauly.bzaar.net/advogato_files/
        graph20041028154056.dot 27-Aug-2007 06:19   2.2M
        graph20051111035647.dot 27-Aug-2007 06:19   2.5M
        graph20060211110033.dot 27-Aug-2007 06:19   3.0M
        graph20060520065443.dot 27-Aug-2007 06:20   3.1M
        graph20070827.dot       27-Aug-2007 06:20   2.5M  
"""

if __name__ == "__main__":
    ROB = RobotsNet()
