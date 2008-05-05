#! /usr/bin/env python
import SOAP
import os.path
from sys import argv

info = ("netFinity.py","0.1")
ident = "%s v%s | Silix.org | the9ull^" % info
DEBUG = False

USAGE = \
"""\
netfinity.py sms [-u|--user user] [-p|--passwd passwd]
           [-d|--dest destinatario[,destinatario1[,...]]]
           [-c|--config file_di_configurazione] [messaggio] [-r|--refresh]

netfinity.py ab|addressbook [-r|--refresh]\
"""

def main():
	data = Data()
	if not data.has_var('u'):
		print "Utente non definito"
		return 1
	if not data.has_var('p'):
		print "Password non definita"
		return 1
	client = Client(data['u'],data['p'])
	
	abl,abd = client.getAddressBook(data.has_var('r'))
	
	if data.action == "sms":
		if not data.has_var('d') or not data['text']:
			print "destinatario o testo non definiti"
			return 2
		#print "'"+data['text']+"'"
		l = data['d'].split(",")
		lenab = len(abl)
		desta = []
		
		for dest in l:
			try:
				intdest = int(dest)
			except ValueError:
				print "Destinatario incorretto:",dest
			
			if intdest<lenab:
				desta.append(abd[abl[intdest]])
			else:
				desta.append(dest)
				#print dest
		
		print client.sendMsg(",".join(desta),data['text'])
	elif data.action == 'ab':
		for contact in abl:
			print contact
	else:
		print ident
		print "USO:",USAGE
		print

class Client:
	def __init__(self,user,passwd):
		self.user = user
		self.passwd = passwd
		self.server = SOAP.SOAPProxy("http://www.silix.org/web_service/netfinity/server2.php")
	def sendMsg(self,dest,text):
		if DEBUG:
			print "DEBUG sendMsg",dest,text.strip()
			return -1
		return self.server.sendUMS(self.user,self.passwd,dest,text.strip(),"%s %s"%info,"1","","0").partition(":")[0]
	def getAddressBook(self,refresh=False):
		if not refresh:
			try:
				f = file(basepath()+"/addressbook","r") #chissa` se funziona su win
				#f = file("addressbook","r") #chissa` se funziona su win
			except IOError:
				return self.getAddressBook(True)
			s = f.read()
			f.close()
		else:
			s = self.server.getAddressBook(self.user,self.passwd)
			f = file(basepath()+"/addressbook","w")
			#f = file("addressbook","w")
			f.write(s)
			f.close()
		
		
		l = s[1:-1].split('","')
		
		f = count = 0
		temp = []
		abl = []
		abd = {}
		for a in l:
			#print f,count,a
			temp.append(a)
			if f == 2:
				#print temp
				k = ("%."+str(ncifre(len(abl)))+"d %s |%s|") % (count,temp[0],temp[2])
				abl.append(k)
				abd[k] = temp[1]
				temp = []
				count += 1
			f = (f+1) % 3
		
		return abl,abd

def ncifre(n):
	if n==0:
		return 0
	else:
		return 1 + ncifre(n/10)

class Data:
	action = None
	config = {}
	def __init__(self):
		self.__params()
		#print "DEBUG params",self.config
		
		if self.config.has_key('c'):
			nome = self.config['c']
		else:
			nome = basepath()+"/netfinity.conf"
			#nome = "netfinity.conf"
		
		self.__config(nome)
		#print "DEBUG config",self.config
	
	#leggo i parametri dalla linea di comando
	def __params(self):
		self.config['text'] = ""
		if argv[1:]:
			if argv[1] == 'addressbook':
				self.action = 'ab'
			else:
				self.action = argv[1]
			k = False
			for arg in argv[2:]:
				if arg[0] == '-':
					k = arg[1:]
					if k == 'r' or k == '-refresh':
						self.config['r'] = False
						k = False
				elif k:
					#print '['+k+']',arg
					if k[0] == '-':
						try:
							k = {
								'-user':'u',
								'-passwd':'p',
								'-dest':'d',
								'-config':'c'
							}[k]
						except KeyError: pass
					self.config[k] = arg
					k = False
				else:
					#print arg
					self.config['text'] += " " + arg

	#legge la configurazione dal .conf
	def __config(self, nome):
		try:
			f = file(nome,"r")
		except IOError:
			return
		for line in f:
			line = line.partition("#")[0].strip()
			if line:
				t = line.partition(" ")
				if t[2]:
					try:
						k = {
							'user':'u',
							'passwd':'p',
							'dest':'d'
						}[t[0]]
					except KeyError:
						k = t[0]
					if not self.config.has_key(k):
						self.config[k] = t[2]
	def has_vars(self,kk):
		for k in kk:
			if not self.config.has_key(k):
				return False
		return True
	def has_var(self,k):
		return self.config.has_key(k)
	def __getitem__(self,item):
		return self.config[item]

def basepath():
	return os.path.realpath(os.path.dirname(argv[0]))

if __name__=="__main__":
	main()

