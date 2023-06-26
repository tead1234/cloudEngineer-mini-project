import pymysql


class DatabaseService:
    def __init__(self, ho, us, passd, d, char):
        self.ho = ho
        self.us = us
        self.passd = passd
        self.d = d
        self.char = char
    
    def getCursor(self):
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def getConn(self):
        self.conn = pymysql.connect(host=self.ho, user=self.us, password=self.passd, db=self.d, charset=self.char)
        return self.conn
    
    def getReviews(self):
        conn = self.getConn()
        cursor = self.getCursor()

        sql = '''
            SELECT * FROM review;
        '''

        cursor.execute(sql)
        rows = cursor.fetchall()
        reviews = [dict(row) for row in rows]

        return reviews