import codecs
import re


de_utf8 = lambda s: codecs.utf_8_decode(s, "ignore")[0]
en_utf8 = lambda s: codecs.utf_8_encode(s, "ignore")[0]
de_latin1 = lambda s: codecs.latin_1_decode(s, "ignore")[0]
class UnicodeProcessor:
	"""Try to do something senseful with unicode stuff."""
	re_unicodexml = re.compile("&#(\d{3,5});")
	def __init__(self, latin1 = False):
		self.repl_unicodexml = lambda x: en_utf8(unichr(int(x.group(1))))
		if latin1:
			self.process = self.process_latin1

	def process_latin1(self, string):
		string = de_latin1(string)
		string = en_utf8(string)
		return re_unicodexml.sub(self.repl_unicodexml, string)

	def process(self, string):
		return re_unicodexml.sub(self.repl_unicodexml, string)
	


re_unicodexml = re.compile("&#(\d{3,5});")
repl_unicodexml = lambda x: en_utf8(unichr(int(x.group(1))))
def to_unicode(string):
	"""Convert Unicode &#xxx; stuff and try to handle other stuff.

	Still doesn't work like it should.  Decoding latin_1 and encoding
	as utf8 seems weird, but leads to better results (i.e. less
	garble). But still there is garble, and it shouldn't be so.
	"""
	#s1 = string
	string = de_latin1(string)
	#s2 = string
	string = en_utf8(string)
	string = re_unicodexml.sub(repl_unicodexml, string)
	return string
