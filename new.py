import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='JATT123 sengh',
                             database='college',
                             cursorclass=pymysql.cursors.DictCursor)
        
        
with connection:
    with connection.cursor() as cursor:
        # Execute a query to list all tables in the database
        query = "SHOW TABLES"
        cursor.execute(query)

    # Fetch all the table names
        tables = cursor.fetchall()

    # Print the table names
        # Extract and print the table names
        table_names = [table_info['Tables_in_' + "college"] for table_info in tables]
        for table_name in table_names:
            print(table_name)
        # Create a new record
    sql = "INSERT INTO `root` (`email`, `password`) VALUES (%s, %s)"
    cursor.execute(sql, ('webmaster@python.org', 'very-secret'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        cursor.execute(sql, ('webmaster@python.org',))
        result = cursor.fetchone()
        print(result)
        
        
        
        