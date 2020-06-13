import mysql.connector
from mysql.connector import Error
import os
from logger import logger

DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')


def get_connection():
    connection = None
    try:
        connection = mysql.connector.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    except Error as e:
        logger.error(e)
    return connection
