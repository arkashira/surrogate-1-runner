import psycopg2
from psycopg2 import pool

connection_pool = None

def init_db_pool():
    global connection_pool
    connection_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host='localhost',
        database='surrogate_db',
        user='surrogate_user',
        password='surrogate_password'
    )

def get_db_connection():
    if connection_pool is None:
        init_db_pool()
    return connection_pool.getconn()

def release_db_connection(conn):
    if connection_pool is not None:
        connection_pool.putconn(conn)