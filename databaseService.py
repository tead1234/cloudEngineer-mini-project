import pymysql


class DatabaseService:
    def __init__(self, ho, us, passd, d, char):
        self.conn = pymysql.connect(host=ho, user=us, password=passd, db=d, charset=char)
        self.cursor = self.conn.cursor()
    
    def getCursor(self):
        return self.cursor
    
    def getConn(self):
        return self.conn