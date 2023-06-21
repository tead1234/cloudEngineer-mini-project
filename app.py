from flask import Flask, render_template, request
from databaseService import databaseService
app = Flask(__name__) # 초기화
@app.route('/') # 요청 주소
def hello_world(): 
    return 'Hello, World!'
@app.route('/menu', methods = ['GET', 'POST']) # 요청 주소
def menu(): 
    return render_template(
        'menu.html'
    )
@app.route('/index', methods =['GET', 'POST']) # 요청 주소
def index():
    ## post 
    if request.method == 'POST':
        form = request.form
        
    return render_template(
        'index.html'
    )

if __name__ == '__main__':
    app.run(debug= True)