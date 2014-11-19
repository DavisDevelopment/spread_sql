import sys


# Base Error Class, from which all other Error classes extend
class BaseError ( object ):
	def __init__(self, message):
		self._message = message
		self.message = property(self.get_message, self.set_message)

	def get_message(self):
		return self._message

	def set_message(self, newvalue):
		pass

	# Equivalent of [toString]
	def __str__(self):
		return self.message

class Error ( BaseError ):
	def __init__(self, msg):
		super(BaseError)