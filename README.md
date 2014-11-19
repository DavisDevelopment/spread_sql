
## spread_sql | A Library for Treating Excel Spreadsheets like Databases ##
---

`spread_sql` was created because I thought it would be cool if one could use SQL queries on spreadsheets.
It's still *very* much in-development, but does show promise as of now.
Right now, it can only read and write spreadsheets; not parse or execute SQL on them, but that feature _is_ in the works.

---
## API ##
---

The `spread_sql` module currently only exposes one useful class.  

### [`class spead_sql.spreadsheets.Sheet`](https://github.com/DavisDevelopment/spread_sql/blob/master/spread_sql/spreadsheets.py#L38) ###
---

#### `function new():Void` ####
`Sheet`'s constructor. Takes no arguments  

#### [`function column(colname:String):Void`](https://github.com/DavisDevelopment/spread_sql/blob/master/spread_sql/spreadsheets.py#L51) ####
Creates a new column.  

`@param colname <String>` - The name of the column to create  

#### [`function row(index:Int):Null<Row>`](https://github.com/DavisDevelopment/spread_sql/blob/master/spread_sql/spreadsheets.py#L56) ####
Retrieves the row at the given index, if it exists  

`@param index <Int>` - The index to search for a row at  

#### [`function insert(row:Dynamic, ?index:Null<Int>):Void`](https://github.com/DavisDevelopment/spread_sql/blob/master/spread_sql/spreadsheets.py#L79) ####
Inserts a new row into the `Sheet`  

`@param row <Dynamic>` - A Dictionary object-representation of the row to create  
`@param index <Int>` - If set, defines a custom index to place the row at  

#### [`function remove_row(index:Int):Void`](https://github.com/DavisDevelopment/spread_sql/blob/master/spread_sql/spreadsheets.py#L105) ####
Deletes a row from the sheet  

`@param index <Int>` - The index of the row to delete  

#### [`function map(lambda:Row->Void):Void`](https://github.com/DavisDevelopment/spread_sql/blob/master/spread_sql/spreadsheets.py#L95) ####
Applies the given function to each row of the `Sheet`.  
Will replace each row with the return-value of `lambda`.  
For instance, to iterate through all rows without changing them, once would type:  

	from spread_sql.spreadsheets import *

	sheet = getSheetInstanceSomehow()
	
	#- lambda-function to apply to all rows
	def alterer(row):
		print row
		return row
	sheet.map( alterer )


`@param lambda <Function>` - The function to apply to each row  

#### [`function remove_column(colname:String):Void`](https://github.com/DavisDevelopment/spread_sql/blob/master/spread_sql/spreadsheets.py#L114) ####
Deletes the given column from the `Sheet`  

`@param colname <String>` - The name of the column to delete  

#### [`function rename_column(old_col:String, new_colname:String):Void`](https://github.com/DavisDevelopment/spread_sql/blob/master/spread_sql/spreadsheets.py#L139) ####
Rename a column in the `Sheet`  

`@param old_col <String>` - The name of the column to rename  
`@param new_col <String>` - What to rename it *to*  

#### [`function save(filename:String):Void`](https://github.com/DavisDevelopment/spread_sql/blob/master/spread_sql/spreadsheets.py#L149) ####
Saves the `Sheet` to a file  

`@param filename <String>` - the path to the file to save it to  

#### [`static function loadXLS(filename:String):Sheet`](https://github.com/DavisDevelopment/spread_sql/blob/master/spread_sql/spreadsheets.py#L242) ####
Loads an XLS document, and returns a `Sheet` object

`@param filename <String>` - the path to the file to load  
`@return <Sheet>`  

#### [`static function fromJSON(data:Array<Dynamic>):Sheet`](https://github.com/DavisDevelopment/spread_sql/blob/master/spread_sql/spreadsheets.py#L220) ####
Creates a `Sheet` instance from a given array of row-objects

`@param data <Array<Dynamic>>` - Array of row-objects  

