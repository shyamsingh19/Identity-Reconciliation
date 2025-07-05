import pymysql
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
db_name = config.get("DATABASE", "DB_NAME")
user = config.get("DATABASE", "USER")
host = config.get("DATABASE", "HOST")
port = config.get("DATABASE", "PORT")
timeout = config.get("DATABASE", "TIMEOUT")
password = config.get("DATABASE", "PASSWORD")


connection = pymysql.connect(
    charset="utf8mb4",
    connect_timeout=int(timeout),
    cursorclass=pymysql.cursors.DictCursor,
    db=db_name,
    host=str(host),
    password=str(password),
    read_timeout=int(timeout),
    port=int(port),
    user=user,
    write_timeout=int(timeout),
    autocommit=True,
)


def get_connection():
    return connection
