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
