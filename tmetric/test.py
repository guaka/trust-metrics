import os
from trustlet import *


def execute(cmd):
    print cmd
    os.system(cmd)


a = Advogato.Advogato("none")
execute("./tmetric < " + a.filepath)
print "What does delta = 0.0000 mean?"
