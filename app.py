from flask import Flask, render_template, request
from databaseService import DatabaseService
app = Flask(__name__) # 초기화
## db 
db = DatabaseService('127.0.0.1',
            'root',
            '1234',
            'cafe_DB',
            'utf8')


@app.route('/') # 요청 주소
def hello_world(): 
    return 'Hello, World!'
@app.route('/menu', methods = ['GET', 'POST']) # 요청 주소g
def menu(): 
    return render_template(
        'menu.html'
    )
@app.route('/index', methods =['GET', 'POST']) # 요청 주소
def index():
    ## post 
    if request.method == 'POST':
        
        form = request.form
        cafeName = form['cafe-name']
        sql = '''
            insert into cafe (id, name,address)
            values(null, %s, null)
        '''
        conn = db.getConn()
        cursor = db.getCursor()
        cursor.execute(sql,(cafeName))
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