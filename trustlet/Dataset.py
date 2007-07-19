
import os

class Network:
    def __init__(self):
        self.path = os.path.join(self.dataset_dir(), self.__class__.__name__)
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def dataset_dir(self):
        if os.environ.has_key('HOME'):
            home = os.environ['HOME']
        self.dataset_path = os.path.join(home, 'datasets')
        if not os.path.exists(self.dataset_path):
            os.mkdir(self.dataset_path)
        return self.dataset_path
        
    def download(self, url, file):
        filepath = os.path.join(self.path, file)
        print "Downloading %s to %s " % (url, filepath)
        import urllib
        p = urllib.urlretrieve(url, filepath)
