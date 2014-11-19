import os, sys, subprocess

platform = os.uname()

# Function to execute shell command, and return output
def runcommand(comm, *args):
	args = list(args)
	p = subprocess.Popen(([comm] + args), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	(outdata, errdata) = p.communicate()

	return outdata

# Determines whether the user has a given command installed
def hascommand(comm):
	return (runcommand('which', comm) != '')




def main():
	print 'cheeks: ' + runcommand(
		'which', 'node'
	)

if __name__ == '__main__':
	main()