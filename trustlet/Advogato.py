#!/usr/bin/env python

__doc__ = """
This is a module implementing the Advogato datasets. There are also
classes to get other datasets based on the mod_virgule code.
"""


from Dataset import Network
from networkx.xdigraph import XDiGraph
import os

class Advogato(Network):
    """The Advogato dataset"""
    
    url = "http://www.advogato.org/person/graph.dot"
    dotfile = 'graph.dot'

    level_map = {
        'Observer': 0.4,
        'Apprentice': 0.6,
        'Journeyer': 0.8,
        'Master': 1.0
        }
    def __init__(self, filename = None, comp_threshold = 0):
        Network.__init__(self)
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
        return self.level_map[edge[2]['level']]

    def download(self, only_if_needed = False):
        if only_if_needed and os.path.exists(self.filepath):
            return
        self.download_file(self.url, self.dotfile)
        self.fix_graphdot()

    def fix_graphdot(self):
        """Fix syntax of graph.dot (8bit -> blah doesn't work!)"""
        import re
        
        print 'Fixing graph.dot'
        f = open(self.filepath, 'r')
        l_names = f.readlines()
        f.close()
        p = re.compile(' (\w+)')
        l_fixed = map(lambda s: p.sub(r' "\1"', s), l_names)

        f = open(self.filepath, 'w')
        f.writelines(l_fixed)
        f.close()
        return self.filepath

    def get_graph_dot(self, filepath = None):
        import networkx
        if not filepath:
            filepath = self.filepath
        print "Reading", filepath, "as a NetworkX graph"
        graph = networkx.read_dot(filepath)

        #beh, read_dot should be method of self, so we can avoid this dirty loop shit
        for node in graph.nodes():
            self.add_node(node)
        for edge in graph.edges():
            self.add_edge(edge)


"""

There are other communities which use the same advogato software
(mod_virgule) and so they have the same trust levels and system and
publish the trust graph.  We created classes for some of them here.

More to add:
 * persone.softwarelibero.org  
      Paolo can probably easily obtain the dataset that is not
      downloadable at the standard person/graph.dot location)

"""

class RobotsNet(Advogato):
    """
    See http://trustlet.org/wiki/Robots.net
    Problem: spaces in graph.dot
    """
    url = "http://robots.net/person/graph.dot"

    def fix_graphdot(self):
        """Fix syntax of graph.dot (8bit -> blah doesn't work!)"""
        import re
        
        print 'Fixing graph.dot'
        
        f = open(self.filepath, 'r')
        l_names = f.readlines()
        f.close()
        p_fixspace = re.compile('(\w) (\w)')
        l_names_spacefix = map(lambda s: p_fixspace.sub(r'\1___\2', s).replace(".", "dot"), l_names)

        p = re.compile(' ([\w\-_]+)')
        l_fixed = map(lambda s: p.sub(r' "\1"', s), l_names_spacefix)

        import pprint
        pprint.pprint (l_fixed)

        f = open(self.filepath + 'test', 'w')
        f.writelines(l_fixed)
        f.close()
        return self.filepath + 'test'

class SqueakFoundation(Advogato):
    """Squeak Foundation dataset"""
    url = "http://people.squeakfoundation.org/person/graph.dot"
    level_map = {  # do these values make sense?
        'violet': 0.4,
        'blue': 0.6,
        'green': 0.8,
        'gray': 1.0
        }

    def trust_on_edge(self, edge):
        return self.level_map[edge[2]['color']]

class Kaitiaki(SqueakFoundation):
    """Kaitaki dataset"""
    url = "http://www.kaitiaki.org.nz/virgule/person/graph.dot"


if __name__ == "__main__":
    import analysis
    rob = RobotsNet()
