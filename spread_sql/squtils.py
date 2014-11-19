import sys
import spreadsheets

# get the name of the class that created the given object
typename = lambda obj: (type(obj).__name__)

"""
 * Row class - basically a dictionary, but doesn't throw errors
"""
class Row ( object ):
	def __init__(self, base={}):
		if typename(base) == 'dict':
			self.base = base
		else:
			self.base = {}

	# determine if the given key is a key of this Row
	def exists(self, key):
		try:
			v = self.base[key]
			return True
		except:
			return False

	def keys(self):
		return [key for key in self.base.keys()]

	# returns the given key of this Row
	def get(self, key):
		if self.exists(key):
			return self.base[key]
		else:
			return None

	# set the given attribute of this Row
	def set(self, key, value):
		self.base[key] = value

	# delete the attribute referenced by [key]
	def remove(self, key):
		del self.base[key]

	"""
	 * Magic-Methods! :D
	"""

	# Controlls property access using the '.' operator
	def __getattr__(self, key):
		return self.get( key )

	# Controls property assignment using the '.' operator
	def __setattr__(self, key, value):
		self.set(key, value)

	# Controls property deletion using the '.' operator
	def __delattr__(self, key):
		self.remove(key)

	# Controls property access using array-access
	def __getitem__(self, key):
		return self.get( key )

	# Controls property assignment using array-access
	def __setitem__(self, key, value):
		return self.set(key, value)

	# Controls property deletion using array-access
	def __delitem__(self, key):
		self.remove(key)
