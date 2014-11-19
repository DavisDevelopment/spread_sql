import sys
import xlutils
import xlrd
import xlwt
import os
import fs
import json
import squtils
import db

from errors import Error

path = os.path

# Get the name of the class that created the given object
typename = lambda obj: (type(obj).__name__)

# Encode to JSON string, then decode to Dictionary, effectively ensuring that type is [dict]
todict = lambda obj: (json.loads(json.dumps(obj)))

# Version number for this file
version = '0.0.1'

# Dictionary which associates format ID integers with their string counterparts
FORMATS = {
	0 : 'xls',
	1 : 'csv',
	2 : 'json'
}

# Book class, for reading/writing workbooks
class Book ( object ):
	def __init__(self):
		self.filename = ''
#		self.

# SpreadSheet class, for reading/writing to/from spreadsheet files
class Sheet ( object ):
	def __init__(self):
		self.filename = ''
		self.name = 'sheet1'

		# List of column names
		self.header = []

		# List of value-tuples
		self.rows = []


	# Add Column to Header
	def column(self, colname):
		self.header.append(colname)

	# Retrieve row from list, in dictionary format
	def row(self, index):
			# Dictionary to be formatted and returned
			ret_dict = {}

			# Value-Tuple found at given index
			tup = list(self.rows[index])

			i = 0

			# For every column-name in the header
			for colname in self.header:
				# grab that value from the tuple, and insert it into the dictionary to be returned
				try:
					ret_dict[colname] = tup[self.header.index(colname)]

				except IndexError:
					#-print ("Found no value at col-{0}, row-{1}".format(i, index))
					pass
				# increment [i] by one
				i += 1

			return ret_dict

	# Insert Row
	def insert(self, row, index=False):
		values = []

		for key in self.header:
			try:
				values.append( row[key] )
			
			except:
				values.append( None )

		if index == False:
			self.rows.append( tuple(values) )
		else:
			self.rows[index] = tuple(values)

	# [map] method to apply a function to each row in the sheet
	def map(self, alterer):
		for index in range(0, len(self.rows)-1):
			row = self.row(index)

			if row != None:
				newrow = alterer(row)

				self.insert(newrow, index)

	# Remove Row from Sheet
	def remove_row(self, index):
		removed = self.rows[index]
		del self.rows[index]
		if removed != None:
			return removed
		else:
			return None

	# Remove column from both header and all rows
	def remove_column(self, colname):
		# Determine the index of [colname] in [header]
		index = self.header.index(colname)

		# Delete [colname] from [header]
		del self.header[index]


		i = 0
		# For each row, remove the value at [index]
		for row in self.rows:
			thisrow = list(row)
			del thisrow[index]

			self.rows[i] = tuple(thisrow)

			i += 1

	# Remove a set of columns from both header and all rows
	def remove_columns(self, colnames):
		# For column-name in [colnames]
		for name in colnames:
			self.remove_column(name)

	# Rename column
	def rename_column(self, old_colname, new_colname):
		# Determine the index of [old_colname] in [header]
		index = self.header.index(old_colname)

		self.header[index] = new_colname




	# Method to save Sheet object to file
	def save(self, filename=False, format=0):

		# name of file to save this Sheet to
		if filename == False:
			filename = self.filename
		else:
			self.filename = filename

		# Figure out what format to save Sheet to
		try:
			fileformat = FORMATS[format]
		except:
			fileformat = FORMATS[0]

		formatter = FORMATTERS[fileformat]

		formatter(self)


	"""
	 * MAGIC METHODS!! :D
	"""

	#= Array-Access =#

	# Array-Getter
	def __getitem__(self, index):
		
		# Retrieve the row at [index]
		if typename(index) == 'int':
			return self.row(index)

		# If [index] is a String
		elif typename(index) == 'str':
			# Treat [index] as a column name, and return an array of that column for every row in this Sheet
			values = []

			for index in range(0, len(self.rows)):
				row = self.row(index)
				if row != None:
					values.append(row[index])
			return values

		# If [index] is a tuple, or a list
		elif typename(index) == 'tuple' or typename(index) == 'list':
			# Convert to list, if not already one, and cap length at 2
			pair = list(index)[0 : 2]

			# Create list of types
			types = [typename(item) for item in pair]

			# If both items in [pair] are integers
			if types[0] == 'int' and types[1] == 'int':
				(y, x) = pair

				return (self.rows[y][x])

			elif types[0] == 'int' and types[1] == 'str':
				(y, colname) = pair

				return (self.row(y)[colname])

			else:
				raise Error("Unsupported array-access")

		else:
			return None

		
# Static Method to create Sheet object from JSON object
	@staticmethod
	def fromJSON( jset ):
		# new Sheet object to be inserted into
		sheet = Sheet()

		# for every entry in the given set
		for entry in jset:
			# for each key-value pair in the entry
			for key in entry.keys():
				value = entry[key]
				# if [key] has not already been inserted into header of [sheet]
				if not (key in sheet.header):
					# insert it now
					sheet.column(key)

			sheet.insert( entry )

		return sheet



	# Static Method to load Sheet object from XLS file
	@staticmethod
	def loadXLS(filename, index = 0):
		sheet = Sheet()

		if path.exists(filename):
			component = xlrd.open_workbook(filename).sheet_by_index(index)

			x = 0
			y = 0
			ecount = 0
			rows = []
			row = []
			while True:
				try:
					value = component.cell_value(y, x)
					row.append(value)
					ecount = 0
					x += 1

				except:
					if ecount == 0:
						x = 0
						y += 1
						ecount += 1

						newrow = tuple(row)
						row = []

						rows.append(newrow)
					else:
						break

			sheet.header = rows[0]
			sheet.rows = rows[1:]
		else:

			raise errors.Error(('Cannot load non-existent file "{0}"' % [filename]))

		return sheet

	# Static Method to load Sheet object from JSON file
	@staticmethod
	def loadJSON(filename):
		content = fs.getContent(filename)
		entryList = json.loads(content)

		return Sheet.fromJSON( entryList )


	# Static method to load Sheet object
	# from SQL-Query results
	@staticmethod
	def loadFromQuery( connection_credentials, sql_string ):
		# initialize new database-connection
		conn = db.DBConn( **connection_credentials )
		
		# Execute sql_string, and return result
		res = conn.query(sql_string)
		print ('\n' * 3)
		print res[0]
		print ('\n' * 3)


# Save sheet to file in XLS format
def save_to_xls(sheet):
	book = xlwt.Workbook()
	newsheet = book.add_sheet(sheet.name)

	rows = ([sheet.header] + list(sheet.rows))

	rown = 0
	coln = 0

	for row in rows:
		for col in row:

			newsheet.write(rown, coln, col)

			coln += 1
		coln = 0
		rown += 1
	book.save(sheet.filename)

# Functions to save Sheet objects to files
FORMATTERS = {
	'xls' : save_to_xls
}


# Declare exported variables
__all__ = [
	'version',
	'Sheet'
]
