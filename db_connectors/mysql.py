import mysql.connector
from mysql.connector import Error

class MySQLConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return True
        except Error as err:
            print(f"Error connecting to MySQL: {err}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        """Execute a SELECT query and return results"""
        if not self.connection or not self.connection.is_connected():
            print("Not connected to MySQL")
            return None
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as err:
            print(f"Query execution error: {err}")
            return None

    def execute_update(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE query"""
        if not self.connection or not self.connection.is_connected():
            print("Not connected to MySQL")
            return False
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        except Error as err:
            print(f"Update execution error: {err}")
            self.connection.rollback()
            return False

# opt/axentx/surrogate-1/db_connectors/mariadb.py
import mariadb
from mariadb import Error

class MariaDBConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Establish connection to MariaDB database"""
        try:
            self.connection = mariadb.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return True
        except Error as err:
            print(f"Error connecting to MariaDB: {err}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        """Execute a SELECT query and return results"""
        if not self.connection:
            print("Not connected to MariaDB")
            return None
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as err:
            print(f"Query execution error: {err}")
            return None

    def execute_update(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE query"""
        if not self.connection:
            print("Not connected to MariaDB")
            return False
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
        except Error as err:
            print(f"Update execution error: {err}")
            self.connection.rollback()
            return False