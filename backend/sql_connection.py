import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling


def get_sql_pool():
    # Initialize connection pool
    # Use connection pooling whenever possible, as it improves performance and scalability.

    # MySQL connection pool configuration
    pool_name = "mypool"
    pool_size = 5  # Number of connections in the pool
    # pool_timeout = 30  # Wait time before throwing error if no connection is available
    pool_reset_session = True  # Reset session after returning the connection to the pool
    # pool_recycle = 3600  # Recycle connection after 1 hour of being idle (3600 seconds).
    # Removing stale connection. Recycling connections ensures that they stay alive and valid.
    """Unfortunately, settings like max_overflow, pool_recycle, and pool_timeout are not natively supported 
    in mysql-connector-python"""

    try:
        db_pool = pooling.MySQLConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            pool_reset_session=pool_reset_session,
            host="localhost",
            database="grocery_store",
            user="root",
            password="Network@17``1234@@"
        )
        return db_pool
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None


# This is only for local testing
def get_sql_connection():

    try:

        # Create a global connection
        db_conn = mysql.connector.connect(
            host="localhost",
            database="grocery_store",
            user="root",
            password="Network@17``1234@@"
        )
        return db_conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        return None