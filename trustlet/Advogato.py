#!/usr/bin/env python

import Dataset
import os

class Advogato(Dataset.Network):
    def __init__(self):
        Dataset.Network.__init__(self)
        self.url = "http://www.advogato.org/person/graph.dot"
        self.file = 'graph.dot'
        self.filepath = os.path.join(self.path, self.file)
        self.numbersfilepath = os.path.join(self.path, 'graph.numbers.dot')
        self.download(only_if_needed = True)

    def download(self, only_if_needed = False):
        if only_if_needed and os.path.exists(self.filepath):
            return
        self.download_file(self.url, self.file)
        self.fix_graphdot()
        # it's really fast, so we just do this as well
        self.numbersfilepath = self.convert_dot_names_into_numbers()

    def load(self):
        import pydot
        self.download(only_if_needed = True)
        print "Loading graph.dot..."
        g = pydot.graph_from_dot_file(self.filepath)

    def fix_graphdot(self):
        '''Fix syntax of graph.dot (8bit -> blah doesn't work!)'''
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
                        replace('Observer"', '0.0'), # Should Observer be 0?
                        l_names)
        newfilename = self.numbersfilepath 
        newfile = open(newfilename, 'w')
        newfile.write("/* fixed node names starting with number */ \n");
        newfile.writelines(l_numbers)
        newfile.close()
        return newfilename
    
if __name__ == "__main__":
    adv = Advogato()
    # adv.convert_dot_names_into_numbers()
            
