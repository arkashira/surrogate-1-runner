
import mysql.connector
import mariadb
from mysql.connector import errorcode
from mariadb import Error

# MySQL connection function
def connect_to_mysql(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    return None

# MariaDB connection function
def connect_to_mariadb(host, user, password, database):
    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )
        return conn
    except Error as e:
        print("Error while connecting to MariaDB", e)
    return None

# Predefined transaction tests
def test_transaction(conn, cursor):
    # Test 1: Insert and retrieve data
    cursor.execute("INSERT INTO test_table (id, value) VALUES (1, 'test')")
    conn.commit()
    cursor.execute("SELECT * FROM test_table WHERE id = 1")
    result = cursor.fetchone()
    assert result is not None, "Test 1 failed: Data not inserted or retrieved"

    # Test 2: Update data
    cursor.execute("UPDATE test_table SET value = 'updated' WHERE id = 1")
    conn.commit()
    cursor.execute("SELECT * FROM test_table WHERE id = 1")
    result = cursor.fetchone()
    assert result[1] == 'updated', "Test 2 failed: Data not updated"

    # Test 3: Delete data
    cursor.execute("DELETE FROM test_table WHERE id = 1")
    conn.commit()
    cursor.execute("SELECT * FROM test_table WHERE id = 1")
    result = cursor.fetchone()
    assert result is None, "Test 3 failed: Data not deleted"

# Compare results and highlight differences (to be implemented)

# Summary:
# - Created MySQL and MariaDB connection functions
# - Added predefined transaction tests
# - Comparison of results and highlighting differences is pending