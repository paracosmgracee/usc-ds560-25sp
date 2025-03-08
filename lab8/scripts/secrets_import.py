import configparser

config = configparser.ConfigParser()
config.read('/Users/liuyuxuan/usc-ds560-25sp/lab8/scripts/.env')

print(config.sections())

MYSQL_HOST=config['mysql']['host']
MYSQL_USER = config['mysql']['user']
MYSQL_PASSWORD = config['mysql']['password']
MYSQL_DB = config['mysql']['database']