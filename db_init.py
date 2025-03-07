import psycopg2

# Python file with sensitive data to make the connection
# the "Credentials" is a simple class inside the file "db_credentials_info.py"
from db_credentials_info import Credentials

c = psycopg2.connect(
    dbname = "postgres",
    user = Credentials.User,
    password = Credentials.Password,
    host = Credentials.Host,
    port = Credentials.Port
)

c.autocommit = True
cursor = c.cursor()
cursor.execute("CREATE DATABASE citricsheep_devtest")
cursor.close()
c.close()
