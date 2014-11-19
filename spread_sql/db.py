import psycopg2 as pgsql
import sys, os
path = os.path

"""
 * class DBConn - custom object representation of database-connection
"""
class DBConn ( object ):
	def __init__(self, **credentials):
		self.condata = credentials
		
		# shorthand variable
		cd = self.condata

		# initialize database connection
		self.conn = pgsql.connect(
			dbname = 'tanmarapps_dev',
			host = '10.30.30.30',

			user = 'manager',
			password = 'ZnAnT123!'
		)
	

	# Method to perform SQL-Query
	def query(self, sql_query):
		# create new cursor
		cur = self.conn.cursor(
		
		)
		
		# execute SQL statement
		cur.execute(sql_query)
		
		# fetch results of the query
		retval = cur.fetchall()
		
		# delete cursor object
		cur.close()

		return retval

	
		



