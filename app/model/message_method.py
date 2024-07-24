import os
import mysql.connector
import mysql.connector.pooling
import logging
from dotenv import load_dotenv

load_dotenv()
# logger = logging.getLogger(__name__)
Format = ' %(asctime)s - %(message)s'
# logging.basicConfig(filename='message_db.log', encoding='utf-8', level=logging.INFO, format=Format)


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

def insert_message(message, cdn_url):
  con = connection()
  cursor = con.cursor(dictionary= True)
  try:
    sql="""INSERT INTO  messages
    (message, image_cdn_url)
    VALUES(%s, %s)"""
    val=(f"{message}", f"{cdn_url}")
    cursor.execute(sql, val)
    con.commit()
    print(f"insert{message} in table message")
    # logger.info(f"insert{message} in table message")
    return {"message" : message, "image_cdn_url" : cdn_url}
  except Exception as e:
    print( f"{e}")
    # logger.warning(f"{e}")
  finally:
    cursor.close()
    con.close()

def get_all_message():
  con = connection()
  cursor = con.cursor(dictionary= True)
  try:
    sql="""SELECT * FROM messages ORDER BY id DESC"""
    cursor.execute(sql,)
    raw_data = cursor.fetchall()
    # logger.info(f"get all message")
    return raw_data
  except Exception as e:
    print(f"{e}")
    # logger.warning(f"{e}")
  finally:
    cursor.close()
    con.close()

def get_all_message():
  con = connection()
  cursor = con.cursor(dictionary= True)
  try:
    sql="""SELECT * FROM messages ORDER BY id DESC"""
    cursor.execute(sql,)
    raw_data = cursor.fetchall()
    # logger.info(f"get all message")
    return raw_data
  except Exception as e:
    print(f"{e}")
    # logger.warning(f"{e}")
  finally:
    cursor.close()
    con.close()
