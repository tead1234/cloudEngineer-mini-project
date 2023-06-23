from flask import Flask, redirect, render_template, request, jsonify, url_for
from databaseService import DatabaseService
app = Flask(__name__) # 초기화

## db 
db = DatabaseService('127.0.0.1',
            'root',
            '1234',
            'cafe_DB',
            'utf8')


@app.route('/') # 요청 주소git 
def hello_world(): 
    return 'Hello, World!'

@app.route('/menu', methods = ['GET', 'POST']) # 요청 주소
def menu(): 
    if request.method == 'GET':
        conn = db.getConn()
        cursor = db.getCursor()

        sql = '''
            SELECT NAME FROM cafe;
        '''  
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        names = [list(rows[x]) for x in range(len(rows))]
        names = sum(names, [])
        # print(names)

      
        
        cursor.execute(sql)
        rows = cursor.fetchall()

        selected_cafe = request.args.get('cafe_id')
        print(selected_cafe)
        
        conn = db.getConn()
        cursor = db.getCursor()
        
        
        select_cafe_sql = '''
                select id from cafe where name = %s;
            '''


        return render_template(
            'menu.html' , names=names
        )
    elif request.method == 'POST':
          conn = db.getConn()
          cursor = db.getCursor()
          
        #   selected_cafe = request.form['cafeName']

        #   select_cafe_sql = '''
        #     select id from cafe where name = %s
        #    '''

        #   cursor.execute(select_cafe_sql, (selected_cafe))
        #   select_cafe_id = cursor.fetchone()
        #   print('--------------',select_cafe_id)

          form = request.form
          name = form['name']
          menu = form['menu']
          taste = form['taste']
          been = form['been']
          amount = form['amount']
          price = form['price']
          rate = form['rate']
          coment = form['cafe-coment']
      
          
          sql = '''
                insert into menu1 (menu_id, name) values (null, %s)
          '''
          
          
          cursor.execute(sql,(menu))
          conn.commit()

          cafe_name_sql = '''
                select id from cafe where name = %s
          '''
          
          cursor.execute(cafe_name_sql, (name))
          cafe_id = cursor.fetchone()

          menu_id_sql = '''
                select menu_id from menu1 where name = %s
            '''
          cursor.execute(menu_id_sql,(menu))
          menu_id = cursor.fetchone()
        
          print(f'------------{menu_id}-')

          cafe_menu_sql = '''
             insert into cafe_menu (cafe_id, cafe_menu_id, menu_id)
             values (%s, %s, %s)
          '''
          cafe_menu_id = int(cafe_id[0])+int(menu_id[0])

          cursor.execute(cafe_menu_sql,(cafe_id, cafe_menu_id, menu_id ))
          conn.commit()

          review_sql = ''' 
            INSERT INTO review (menu_id, review_id,  taste, bean, amount, price, rate)
            VALUES (%s, null,  %s, %s, %s, %s, %s)
            '''
          cursor.execute(review_sql, (menu_id, taste, been, amount, price, rate))
          conn.commit()


         



          return redirect(url_for('menu'))

    else:
        return render_template(
            'menu.html'
            )
    
    
@app.route('/admin', methods = ['GET', 'POST']) # 요청 주소
def admin():
    return render_template(
        'admin.html'
    )
## cafe 
@app.route('/regist/delete/<int:id>', methods =['GET']) # 요청 주소
def regitst_delete(id):
    sql =  '''
        delete from cafe
        where id = %s
    '''
    conn = db.getConn()
    cursor = db.getCursor()
    cursor.execute(sql, (id,))
    conn.commit()
    return render_template(
        'registRequest.html'
    )


@app.route('/registRequest', methods =['GET', 'POST']) # 요청 주소
def regist():
    sql =  '''
        select * from cafe join 
        service
        on cafe.id = service.cafe_id
        
    '''
    conn = db.getConn()
    cursor = db.getCursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    print('res', res)
    l  = [list(r) for r in res]
    # for i in l:
    #     i[0] = f'[ id : {i[0]} ]'
    print(l)
    return render_template(
        'resgistRequest.html',
        l = jsonify(l).json
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
        conn.commit()
        searchSql = '''
            select id from cafe where name = %s
        '''
        cursor.execute(searchSql,(cafeName, ))
        cafe_id = cursor.fetchone()[0]
        sql = '''
            insert into service (id,atmosphere, tableCnt, service_time,cafe_id)
            values(null, %s, %s, %s, %s)
        '''
        cursor.execute(sql,(atmo, table, time, cafe_id))
        
        conn.commit()
        # cursor.close()
        # conn.close()
        
        return render_template(
            'index.html'
        )

    else:    

        return render_template(
            'index.html'
        )
    
    

if __name__ == '__main__':
    app.run(debug= True)