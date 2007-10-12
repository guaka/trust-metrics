"""
A simple Table class for the console.

Based on code found at
http://mail.python.org/pipermail/python-list/2003-September/223145.html
"""

class Table:
    """A simple Table class for the console."""
    seps = '- +|'
    
    def __init__(self, columnWidths):
        if columnWidths:
             self._setWidths(tuple(columnWidths))

    def _setWidths(self, columnWidths):
        self.columnWidths = columnWidths
        format1 = ("%%%%-%ss%%s"*len(columnWidths))[:-3]
        format2 = format1 % columnWidths
        self.nSeps = len(columnWidths) - 1
        self.hdrFormat = format2 % ((self.seps[1], )*self.nSeps)
        self.sepFormat = format2 % ((self.seps[2], )*self.nSeps)
        self.rowFormat = format2 % ((self.seps[3], )*self.nSeps)

    def printHdr(self, heading):
        print self.hdrFormat % tuple(heading)

    def printSep(self):
        print self.sepFormat % tuple([self.seps[0]*w for w in self.columnWidths])

    def printRow(self, items):
        print self.rowFormat % tuple(items)

if __name__ == "__main__":
    tbl = Table((12, 12, 16))
    tbl.printHdr(('Item:', 'Value:', 'Another Value:'))
    tbl.printSep()
    tbl.printRow(('a', 1, 2))
    tbl.printRow(('bbbbbbb', 2, 17))
    tbl.printRow(['cc', 3, 5])
