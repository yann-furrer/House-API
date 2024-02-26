import psycopg2
import os 
from dotenv import load_dotenv
load_dotenv()


# Define your connection parameters
dbname = os.getenv('DB')
user = os.getenv('DBUSER')
password = os.getenv('PASSWORD')
host = os.getenv('HOST')
port = os.getenv('PORT')
# Create a connection to the database
try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host
    )
    print("Connected to the database successfully")

    # Create a cursor object
    cur = conn.cursor()
    
    # # Execute a query
    # cur.execute("SELECT version();")

    # # Fetch and print the result of the query
    # db_version = cur.fetchone()
    # print(db_version)

    # # Close the cursor and connection
    #cur.close()
    #conn.close()

except psycopg2.Error as e:
    print(f"Unable to connect to the database: {e}")
