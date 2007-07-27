#!/usr/bin/env python

import Dataset
import os

class Advogato(Dataset.Network):
    def __init__(self):
        Dataset.Network.__init__(self)
        self.url = "http://www.advogato.org/person/graph.dot"
        self.file = 'graph.dot'
        self.filepath = os.path.join(self.path, self.file)
        
    def download(self):
        self.download_file(self.url, self.file)
        # it's really fast, so we just do this as well
        self.numbersfilepath = self.convert_dot_names_into_numbers()

    def load(self):
        import pydot
        if not os.path.exists(self.filepath):
            self.download()
        print "Loading graph.dot..."
        g = pydot.graph_from_dot_file(self.filepath)
    
    def convert_dot_names_into_numbers(self):
        '''Really fast stuff to convert certificate levels from graph.dot into numbers.'''
        print 'Quickly converting graph.dot into graph.numbers.dot'
        f = open(self.filepath)
        l_names = f.readlines()
        l_numbers = map(lambda s:
                        s.replace('level="', '').
                        replace('Master"', '1.0').
                        replace('Journeyer"', '0.8').
                        replace('Apprentice"', '0.6'),
                        l_names)
        newfilename = os.path.join(self.path, 'graph.numbers.dot)')
        newfile = open(newfilename, 'w')
        newfile.writelines(l_numbers)
        newfile.close()
        return newfilename
    
if __name__ == "__main__":
    adv = Advogato()
    adv.download()
    # adv.load()
            
