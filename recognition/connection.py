import mysql.connector

from mysql.connector import Error, MySQLConnection
import os
from logger import logger


def get_connection():
    HOST = os.environ.get('DB_HOST')
    DATABASE = os.environ.get('DB_NAME')
    USER = os.environ.get('DB_USER')
    PASSWORD = os.environ.get('DB_PASSWORD')
    connection = None
    try:
        connection = mysql.connector.connect(host=HOST,
                                             database=DATABASE,
                                             user=USER,
                                             password=PASSWORD)
    except MySQLConnection:
        logger.error("MySQL Connection error")

    return connection
