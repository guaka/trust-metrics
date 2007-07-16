import os, urllib


def download_dotfile():
    from urllib import urlopen
    url = "http://www.advogato.org/person/graph.dot"
    if not os.path.exists("datasets"):
        os.mkdir("datasets")
    if not os.path.exists("datasets/advogato"):
        os.mkdir("datasets/advogato")
    p = urllib.urlretrieve(url, "datasets/advogato/graph.dot")

