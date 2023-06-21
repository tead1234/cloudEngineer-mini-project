import pymysql

class databaseService:
    def __init__(self, ho, us, pass,d, char):
        conn = pymysql.connect(host=ho, user= us, password= pass,
            db= d, charset= char)
        return conn.cursor()