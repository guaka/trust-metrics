"""
A simple Table class for the console.

Based on code written by Bob Gailer <bgailer at alum.rpi.edu>, found
at http://mail.python.org/pipermail/python-list/2003-September/223145.html
and used with permission.

"""

class Table:
    """A simple Table class for the console."""
    seps = '-|+|'
    
    def __init__(self, column_widths):
        if column_widths:
            self._setWidths(tuple(column_widths))

    def _setWidths(self, column_widths):
        self.column_widths = column_widths
        format1 = ("%%%%-%ss%%s"*len(column_widths))[:-3]
        format2 = format1 % column_widths
        self.nSeps = len(column_widths) - 1
        self.hdr_format = format2 % ((self.seps[1],) * self.nSeps)
        self.sep_format = format2 % ((self.seps[2],) * self.nSeps)
        self.row_format = format2 % ((self.seps[3],) * self.nSeps)

    def printHdr(self, heading):
        print self.hdr_format % tuple([s[:w] for w,s in zip(self.column_widths, heading)])

    def printSep(self):
        print self.sep_format % tuple([self.seps[0]*w for w in self.column_widths])

    def printRow(self, items):
        print self.row_format % tuple(items)

if __name__ == "__main__":
    tbl = Table((12, 12, 16))
    tbl.printHdr(('Item:', 'Value:', 'Another Value:'))
    tbl.printSep()
    tbl.printRow(('a', 1, 2))
    tbl.printRow(('bbbbbbb', 2, 17))
    tbl.printRow(['cc', 3, 5])
