from genericpath import exists
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
            
            query='''INSERT INTO orders VALUES (%(action)s,%(symbol)s ,%(price)s ,%(shares)s ,%(datetime)s ); '''
            self.__cursor.execute(query, data)
            self.__conn.commit()
        except Error  as err:
            log.error(err)
            log.error('insert_order')
            
    def update_shares(self, data):
        try:
            print(data)
            operation = "+" 
            if data["action"] != "buy":
                operation = "-"
            query = ''' SELECT COUNT(*) AS total FROM shares WHERE   symbol = %(symbol)s'''
            self.__cursor.execute(query, data)
            exists = self.__cursor.fetchone()
            print(exists)
            if exists["total"] != 0:
                query='''UPDATE shares SET amount = amount {} {} WHERE symbol = %(symbol)s '''.format(operation, data["shares"])
            else:
                query = '''INSERT INTO shares VALUES ( %(shares)s, %(symbol)s);'''
            print(query)
            
            self.__cursor.execute(query, data)
            self.__conn.commit()
        except Error  as err:
            log.error(err)
            log.error('update_shares')
    
    def get_status(self,data):
        try:
            shares = self.get_shares(data)
            historical = self.get_historical(data)
            
            return {"shares": shares, "historical": historical}  
        except Error as err:
            log.error(err)
            log.error('get_status')
    
    def get_shares(self,data):
        try:
            query = ''' SELECT * FROM shares WHERE  symbol=%(symbol)s;'''
            self.__cursor.execute(query, data)
            result = self.__cursor.fetchone()
            return result  
        except Error as err:
            log.error(err)
            log.error('get_shares')
    
    def get_historical(self,data):
        try:
            query = '''SELECT * FROM orders WHERE symbol=%(symbol)s and action="buy";'''
            self.__cursor.execute(query, data)
            result = self.__cursor.fetchall()
            return result  
        except Error as err:
            log.error(err)
            log.error('get_historical')

    