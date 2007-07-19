#!/usr/bin/env python

import Dataset

class Advogato(Dataset.Network):

    def load_network(self):
        self.download_dotfile()

    def download_dotfile(self):
        url = "http://www.advogato.org/person/graph.dot"
        import os
        path = os.path
        if os.environ.has_key('HOME'):
            home = os.environ['HOME']
        dataset_path = path.join(home, "datasets")
        if not os.path.exists(dataset_path):
            os.mkdir(dataset_path)
        adv_path = path.join(dataset_path, 'advogato')
        if not os.path.exists(adv_path):
            os.mkdir(adv_path)
        import urllib
        p = urllib.urlretrieve(url, path.join(adv_path, 'graph.dot'))


if __name__ == "__main__":
    a = Advogato()
    a.load_network()
            
