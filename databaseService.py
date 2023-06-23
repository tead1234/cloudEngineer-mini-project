import pymysql


class DatabaseService:
    def __init__(self, ho, us, passd, d, char):
        self.conn = pymysql.connect(host=ho, user=us, password=passd, db=d, charset=char)
        self.cursor = self.conn.cursor()
    
    def getCursor(self):
        return self.cursor
    
    def getConn(self):
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