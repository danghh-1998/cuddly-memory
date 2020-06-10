import mysql.connector
from mysql.connector import Error
import os
from logger import logger


def get_connection():
    HOST = os.environ.get('DB_HOST')
    DATABASE = os.environ.get('DB_NAME')
    USER = os.environ.get('DB_USER')
    print(os.environ.get('DB_HOST'))
    PASSWORD = os.environ.get('DB_PASSWORD')
    connection = None
    try:
        connection = mysql.connector.connect(host=HOST,
                                             database=DATABASE,
                                             user=USER,
                                             password=PASSWORD)
    except Error as e:
        logger.error(e)

    return connection
