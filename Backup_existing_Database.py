'''
This script takes the backup of exsisting database.
This creates the backup of database and data in it in form of sql statements.
Create table statements of tables and insert statements of data in the database.

requirements:
    python3 or greater
	pymysql

'''



import pymysql
import os

def ExecuteQuery(DB,Query,host,username,password):
	db = pymysql.connect(host,username,password,DB )
	cursor = db.cursor()	
	cursor.execute(Query)
	dataToReturn = cursor.fetchall()
	return dataToReturn

def CheckInstanceOf(ipStr):
	if not ipStr:
		return "NULL"
	if isinstance(ipStr,str):
		return "'"+ipStr+"'"
	else:
		return ipStr

database = input("Enter The Database Name : ")
host = input("Enter The host Name : (localhost) ")
username = input("Enter The user Name : ")
password = input("Enter The password : ")

data = ExecuteQuery("information_schema","select table_name from tables where table_schema='"+database+"' order by CREATE_TIME;",host,username,password)
fo =  open(database+".sql","w+")
fo.write("drop database "+database+";\n\nCreate database "+database+";\n\nUse "+database+";\n\n")
fo.close()

for row in data:
	print (row[0])

	data = ExecuteQuery("information_schema","SELECT 'CREATE TABLE "+row[0]+" (' create_table_statement \
	 UNION ALL \
	 SELECT cols.txt \
	 FROM \
	 (SELECT concat(' ',column_name, ' ', column_type,\
			CASE\
				WHEN is_nullable = 'NO' THEN ' not null'\
				ELSE ''\
			END,\
			CASE\
				WHEN extra IS NOT NULL THEN concat(' ', extra)\
				ELSE ''\
			END,\
			CASE\
				WHEN COLUMN_KEY='UNI' then ' UNIQUE '\
				else ''\
			END,\
	  	',') txt\
	  FROM information_schema.columns\
	  WHERE table_schema = '"+database+"' AND table_name = '"+row[0]+"'\
	  ORDER BY ordinal_position\
	 ) cols\
	\
	UNION ALL\
	 SELECT concat(' constraint primary key (')\
	 FROM information_schema.table_constraints\
	 WHERE table_schema = '"+database+"' AND table_name = '"+row[0]+"'\
	 AND constraint_type = 'PRIMARY KEY'\
	UNION ALL\
	 SELECT cols.txt\
	 FROM (SELECT concat(\
				CASE\
				   WHEN ordinal_position > 1 THEN ' ,'\
				   ELSE ''\
				END, column_name\
			) txt\
			FROM information_schema.key_column_usage\
			WHERE table_schema = '"+database+"' AND table_name = '"+row[0]+"'\
			AND constraint_name = 'PRIMARY'\
			ORDER BY ordinal_position\
	 	) cols \
	UNION ALL\
	 SELECT ' )'\
	UNION ALL\
		SELECT cols.txt	\
		FROM\
			( SELECT concat(', constraint foreign key (',column_name,') references ',T1.REFERENCED_TABLE_NAME,'(',T1.REFERENCED_COLUMN_NAME,')',\
			CASE \
				WHEN UPDATE_RULE='CASCADE ' THEN ' ON UPDATE CASCADE ' ELSE ' ON UPDATE NO ACTION '  END,\
			CASE \
				WHEN DELETE_RULE='CASCADE ' THEN ' ON DELETE CASCADE ' ELSE ' ON DELETE NO ACTION ' END\
)txt\
			FROM information_schema.key_column_usage T1 inner join information_schema.REFERENTIAL_CONSTRAINTS T2\
			on T1.CONSTRAINT_NAME=T2.CONSTRAINT_NAME\
			WHERE T1.table_schema = '"+database+"' AND T1.table_name = '"+row[0]+"'\
			AND T1.REFERENCED_TABLE_NAME !=''\
			ORDER BY ordinal_position ) cols\
\
	 UNION ALL\
	 SELECT ');'",host,username,password)
	
	for row1 in data:
		fo =  open(database+".sql","a+")	
		fo.write(str(row1[0])+"\n\n")
		fo.close()

data=ExecuteQuery(database,"Show Tables;",host,username,password)
for row in data:
	columns = ExecuteQuery(database,"select * from "+row[0],host,username,password)
	if len(columns)>0:
		tableInfo="Insert Into "+row[0]+" Values"
		for col in columns:
			val="("
			for Rdata in col:
				Rdata=CheckInstanceOf(Rdata)
				val=val+str(Rdata)+","
			val=val.strip(",")			
			val=val+")\n,"
			tableInfo=tableInfo+val
		tableInfo=tableInfo.strip(",")
		tableInfo=tableInfo+";"
		fo =  open(database+".sql","a+")	
		fo.write(tableInfo+"\n")
		fo.close()

