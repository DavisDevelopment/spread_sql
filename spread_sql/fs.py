import sys, os
path = os.path

# Check if file or directory exists at given path
exists = lambda name: path.exists(name)

def getContent(name):
	f = open(name, 'r', 1)
	content = f.read()
	f.close()
	return content