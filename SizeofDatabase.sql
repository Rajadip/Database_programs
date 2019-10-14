/*
 This file contains various sql Queries which will
 give you the size of databases in various manners

 MySQL5.7 and MariaDB10.1

 */
/************For Perticular Database*******************/
SELECT
      table_name AS `Table`,
      round(((data_length + index_length) / 1024 / 1024), 4) `Size in MB`
  FROM information_schema.TABLES
  WHERE table_schema = 'Database_name';
/********************************/

/**************data sizex along with index ******************/
SELECT TABLE_NAME, table_rows, data_length, index_length, 
round(((data_length + index_length) / 1024 / 1024),4) "Size in MB",
round(((index_length) / 1024 / 1024),4) "Index in MB",
round(((data_length) / 1024 / 1024),4) "Data in MB"
FROM information_schema.TABLES WHERE table_schema = "Database"
ORDER BY (data_length + index_length) DESC;
/********************************/

/************Sizes of all databases on system********************/
SELECT table_schema                                        "DB Name", 
   Round(Sum(data_length + index_length) / 1024 / 1024, 1) "DB Size in MB" 
FROM   information_schema.tables 
GROUP  BY table_schema;
/********************************/

/************** sizes of databases with free space  ******************/
SELECT table_schema "Data Base Name",
    sum( data_length + index_length ) / 1024 / 1024 "Data Base Size in MB",
    sum( data_free )/ 1024 / 1024 "Free Space in MB"
FROM information_schema.TABLES
GROUP BY table_schema ; 
/******************************** /
