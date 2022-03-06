from .logger import log
from mysql.connector import Error, errorcode, connect

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
class DataBase(metaclass=Singleton):
    __conn = None
    __cursor = None
    __config = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "123456ABC",
        "database": "vest",
        "port": 3307,
    }
    def __init__(self):
        self.__connect()
        
    def __connect(self):
        try:
            cnx = connect(**self.__config)
            self.__conn = cnx
            self.__cursor = cnx.cursor(dictionary=True)
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                log.error('ER_ACCESS_DENIED_ERROR')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                log.error('ER_BAD_DB_ERROR')
                
    def update_status(self, data):
        self.insert_order(data)
        self.update_shares(data)
    
    def insert_order(self, data):
        try:
            operation = "+" 
            if data["action"] != "buy":
                operation = "-"
            query='''INSERT INTO orders VALUES (%(action)s,%(symbol)s ,%(price)s ,%(shares)s ,%(datetime)s ); '''
            self.__cursor.execute(query, data)
            self.__conn.commit()
        except Error  as err:
            log.error(err)
            log.error('insert_order')
            
    def update_shares(self, data):
        try:
            operation = "+" 
            if data["action"] != "buy":
                operation = "-"
            query='''UPDATE shares SET amount = amount {} {} WHERE symbol = %(symbol)s '''.format(operation, data["shares"])
            self.__cursor.execute(query, data)
            self.__conn.commit()
        except Error  as err:
            log.error(err)
            log.error('update_shares')