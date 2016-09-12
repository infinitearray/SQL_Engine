# SQL_Engine

### To run the sql-engine
    * python main.py "<sql-query>"

#### The SQL engine can handle
    * select all records
        usage : "select * from table_name;"
    * Aggregate functions like sum,average,min,max
        usage : "select avg(col) from table_name;"
    * Project columns
        usage : "select col1,col2 from table_name;"
    * Where conditions seperated by AND/OR
        usage : "select col1,col2 from table_name where col1=10 and col2=20;"
    * Projections using one join condition
        usage : "select col1,col2 from table1,table2 where table1.col1=table2.col2;"

#### It could handle some errors like
     * The sql-query should be given as an argument
     * The table_name.csv must exist
     * If table1,table2 have a column a then query cannot be "select a from table1,table2;"
        but we can use "select a from table1;"
     * Aggregate functions cannot be projected with other columns
        i.e "select sum(col1),col2 from table_name;" canot be done
