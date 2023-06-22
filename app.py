from flask import Flask, render_template, request
from databaseService import DatabaseService
app = Flask(__name__) # 초기화
## db 
db = DatabaseService('127.0.0.1',
            'root',
            '1234',
            'cafe_DB',
            'utf8')


@app.route('/') # 요청 주소git l
def hello_world(): 
    return 'Hello, World!'
@app.route('/menu', methods = ['GET', 'POST']) # 요청 주소g
def menu(): 
    return render_template(
        'menu.html'
    )
@app.route('/admin', methods =['GET', 'POST']) # 요청 주소
def admin():
    return render_template(
        'admin.html'
    )
@app.route('/registRequest', methods =['GET', 'POST']) # 요청 주소
def regist():
    return render_template(
        'registRequest.html'
    )


@app.route('/index', methods =['GET', 'POST']) # 요청 주소
def index():
    ## post 
    if request.method == 'POST':
        
        form = request.form
        cafeName = form['cafe-name']
        cafeAddr = form['address']
        atmo = form['atmospher']
        table = form['tableCnt']
        time = form['time']

        sql = '''
            insert into cafe (id, name,address)
            values(null, %s, %s)
        '''
        conn = db.getConn()
        cursor = db.getCursor()
        cursor.execute(sql,(cafeName, cafeAddr))
        searchSql = '''
            select id from cafe where name = %s
        '''
        cafe_id = str(cursor.execute(searchSql,(cafeName)))

        sql = '''
            insert into service (id,atmosphere, tableCnt, service_time,cafe_id)
            values(null, %s, %s, %s, %s)
        '''
        cursor.execute(sql,(atmo, table, time, cafe_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return render_template(
            'index.html'
        )

    else:    

        return render_template(
            'index.html'
        )

if __name__ == '__main__':
    app.run(debug= True)