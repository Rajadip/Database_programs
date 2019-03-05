/*
 This Script gives total data(data+index), only data(data), indexed data(index)
 tablewise, for given database.

 The data sizes are in MB
 */

SELECT table_name AS "Table", 
	round(((data_length + index_length) / 1024 / 1024), 2) as Total Data ,
	round(((data_length) / 1024 / 1024), 2) AS DATA, 
	round((index_length) / 1024 / 1024) as INDEXSIZE 
FROM information_schema.TABLES WHERE table_schema = "Database Name";
