import psycopg2 as pgsql
import sys, os
path = os.path

# Connection-data string, pretty
connection_data = """
dbname=tanmarapps_dev
host=10.30.30.30

user=manager
password=ZnAnT123!
"""

# Now format the data properly
connection_data = [piece.strip() for piece in connection_data.split('\n')]
connection_data = (' '.join(connection_data))

# main function
def main():
	# create a new connection
	conn = pgsql.connect(connection_data)
	

	# get a cursor object
	cur = conn.cursor()

	# execute query
	cur.execute('SELECT * from employees_view')

	# print results

	print cur.fetchall()

if __name__ == '__main__':
	main()






