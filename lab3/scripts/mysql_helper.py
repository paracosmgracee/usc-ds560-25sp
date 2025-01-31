import configparser
import mysql.connector

config = configparser.ConfigParser()
config.read('/home/shubhamdarekar/DSCI560---Shubham/Lab_3/.config')

def create_connection():
    connection = mysql.connector.connect(host=config['mysql']['host'],
                                         user = config['mysql']['user'],
                                         password = config['mysql']['password'],
                                         database = config['mysql']['database'])
    
    return connection

def execute_query(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

def commit_and_close(connection):
    connection.commit()
    connection.close()