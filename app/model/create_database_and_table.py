import os
import mysql.connector
import mysql.connector.pooling
import logging
from dotenv import load_dotenv

load_dotenv()


def create_database():
  mydb = mysql.connector.connect(
    host = os.getenv("DBHOST"),
    user = os.getenv("DBUSER"),
    password = os.getenv("DBPASSWORD"),
  )
  cursor = mydb.cursor()
  cursor.execute("""CREATE DATABASE base_work""")
  cursor.close()
  mydb.close()
  
def connection():
  try:
    dbconfig = {
        "host": os.getenv("DBHOST"),
        "user": os.getenv("DBUSER"),
        "password": os.getenv("DBPASSWORD"),
        "database":"base_work",
    }
    cnxpool = mysql.connector.pooling.MySQLConnectionPool(
      pool_name="mypool",
      pool_size=3,
      **dbconfig
    )
    cnx1 = cnxpool.get_connection()
    return cnx1
  except Exception as e:
    print(f"{e} in create_message_table_def_connection")

def create_table_messages():
  con = connection()
  cursor = con.cursor(dictionary=True)
  try:
    sql = """CREATE TABLE messages(
     id bigint auto_increment,
     message varchar(225),
     image_cdn_url varchar(500),
     primary key(id)
     );
    """
    cursor.execute(sql,)
    
  except Exception as e:
    print(f"{e} in def create_table_messages")
  finally:
    cursor.close()
    con.close()

create_database()
create_table_messages()