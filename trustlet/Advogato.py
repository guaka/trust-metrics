#!/usr/bin/env python

__doc__ = """
This is a module implementing the Advogato datasets. There are also
classes to get other datasets based on the mod_virgule code.
"""


from Dataset import Network
from networkx.xdigraph import XDiGraph
from networkx import component
import os

class Advogato(Network):
    url = "http://www.advogato.org/person/graph.dot"
    dotfile = 'graph.dot'
    def __init__(self, option = True, comp_threshold = 0):
        Network.__init__(self)
        self.filepath = os.path.join(self.path, self.dotfile)
        self.download(only_if_needed = True)

        # ugly, temp workaround: RobotsNet isn't parsing properly yet
        if (self.__class__.__name__ == "RobotsNet"):
            self.fix_graphdot()

        self.numbersfilepath = os.path.join(self.path, self.dotfile.replace('graph.dot', 'numbers.graph.dot'))
        if not os.path.exists(self.numbersfilepath):
            self.convert_dot_names_into_numbers()

        if option == "tiny":
            self.get_graph_dot("tiny_graph.dot")
        elif option:
            self.get_graph_dot()

        if comp_threshold:
            self.ditch_components(comp_threshold)

    def trust_on_edge(self, edge):
        return float(edge[2]['level'])

    def ditch_components(self, threshold = 3):
        UG = self.to_undirected()
        concom_subgraphs = component.connected_component_subgraphs(UG)[1:]
        n_remove = 0
        for sg in concom_subgraphs:
            if len(sg) <= threshold:
                for n in sg:
                    n_remove += 1
                    # print n,
                    self.delete_node(n)
        print "Thrown out", n_remove, "nodes, fraction: ", 1.0 * n_remove / len(UG)

        
    def download(self, only_if_needed = False):
        if only_if_needed and os.path.exists(self.filepath):
            return
        self.download_file(self.url, self.dotfile)
        self.fix_graphdot()

    def load(self):
        import pydot
        self.download(only_if_needed = True)
        print "Loading graph.dot..."
        g = pydot.graph_from_dot_file(self.filepath)

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

    def convert_dot_names_into_numbers(self):
        '''Really fast stuff to convert certificate levels from graph.dot into numbers.'''
        print 'Quickly converting graph.dot into graph.numbers.dot'
        f = open(self.filepath)
        l_names = f.readlines()
        l_numbers = map(lambda s:
                        s.replace('level="', 'level=').
                        replace('Master"', '1.0').
                        replace('Journeyer"', '0.8').
                        replace('Apprentice"', '0.6').
                        replace('Observer"', '0.4'), # Should Observer be 0?
                        l_names)
        newfilename = self.numbersfilepath 
        newfile = open(newfilename, 'w')
        newfile.write("/* fixed node names starting with number */ \n");
        newfile.writelines(l_numbers)
        newfile.close()
        return newfilename

    def get_graph_dot(self, filepath = None):
        import networkx
        if not filepath:
            filepath = self.numbersfilepath
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
    def __init__(self, option = True, comp_threshold = 0):
        Advogato.__init__(self, option, comp_threshold)


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
    def __init__(self, option = True, comp_threshold = 0):
        Advogato.__init__(self, option, comp_threshold)

class Kaitiaki(Advogato):
    url = "http://www.kaitiaki.org.nz/virgule/person/graph.dot"
    def __init__(self, option = True, comp_threshold = 0):
        Advogato.__init__(self, option, comp_threshold)
    
    def trust_on_edge(self, edge):
        color = edge[2]['color']
        # just some uneducated guesses here:
        if color == 'green':
            return 0.8
        elif color == 'blue':
            return 0.6
        elif color == 'gray':
            return 0.2
        elif color == 'violet':
            return 0.4
        return 0.0

        


if __name__ == "__main__":
    import analysis
    rob = RobotsNet()
