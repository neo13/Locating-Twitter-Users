from os import listdir
from os.path import isfile, join, getsize

class File(object):
	def __init__(self):
		super(File, self).__init__()
	
	@staticmethod
	def getFile():
		directory = "./temp/"
		onlyfiles = [ f for f in listdir(directory) if isfile(join(directory,f)) ]
		onlyfiles.sort()
		if len(onlyfiles) == 0 :
			return open(join(directory,str(0)), "a")
		if getsize(join(directory,onlyfiles[-1])) > long(15728640) :
			return open(join(directory,str(int(onlyfiles[-1]) + 1)), "a")
		else:
			return open(join(directory,onlyfiles[-1]), "a")

	@staticmethod
	def write(value):
		f = File.getFile()
		f.write(value)
		f.close()