import configparser
config = configparser.ConfigParser()
config.read('D:\\USC\\DSCI560 - Shubham\\Lab_6\\.env')

MYSQL_HOST=config['mysql']['host']
MYSQL_USER = config['mysql']['user']
MYSQL_PASSWORD = config['mysql']['password']
MYSQL_DB = config['mysql']['database']