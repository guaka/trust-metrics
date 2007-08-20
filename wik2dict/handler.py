import xml.sax
import xml.sax.handler
import pprint
 
class MWHandler(xml.sax.handler.ContentHandler):
  def __init__(self):
    self.inTitle = 0
    self.mapping = {}
 
  def startElement(self, name, attributes):
    if name == "title":
      print name, attributes
      self.buffer = ""
      #self.isbn = attributes["isbn"]
    elif name == "title":
      self.inTitle = 1
 
  def characters(self, data):
    self.data = data
    pprint.pprint(self.data)

    if self.inTitle:
      self.buffer += data
 
  def endElement(self, name):
    if name == "page":
      self.inTitle = 0
      self.mapping[self.buffer] = self.buffer
 

parser = xml.sax.make_parser()
handler = MWHandler()
parser.setContentHandler(handler)
parser.parse("test.xml")

pprint.pprint (parser.data)
