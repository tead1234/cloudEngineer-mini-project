from flask import Flask, redirect, render_template, request, jsonify, url_for
from databaseService import DatabaseService
app = Flask(__name__) # 초기화

## db 
db = DatabaseService('127.0.0.1',
            'root',
            '1234',
            'cafe_DB',
            'utf8')


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
        cursor.close()
        conn.close()
        names = [list(rows[x]) for x in range(len(rows))]
        names = sum(names, [])



        selected_cafe = request.args.get('cafe_review')
        
        conn = db.getConn()
        cursor = db.getCursor()
        
        
        select_cafe_sql = '''
                select id from cafe where name = %s;
            '''

        cursor.execute(select_cafe_sql, (selected_cafe, ))
        rows = cursor.fetchone()
        cursor.close()
        conn.close()
        cafe_id = rows
        conn = db.getConn()
        cursor = db.getCursor()
        select_review_sql = '''
            SELECT  m.name, r.taste, r.bean, r.rate, r.amount, r.price  FROM cafe AS c
            JOIN cafe_menu AS cm
            ON c.id = cm.cafe_id
            JOIN menu1 AS m
            ON cm.menu_id = m.menu_id
            JOIN review AS r
            ON cm.cafe_menu_id = r.cafe_menu_id
            WHERE c.id = %s ;
        '''

        cursor.execute(select_review_sql, (cafe_id, ))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        reviews = [list(rows[x]) for x in range(len(rows))]
        print(reviews)

        return render_template(
            'menu.html' , names=names, reviews=reviews
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
          # coment = form['cafe-coment']
          
          query = "SELECT COUNT(*) FROM menu1 WHERE name = %s"
          cursor.execute(query, (menu,))
          count = cursor.fetchone()[0]
          
        ## insert menu
          if count == 0:
    # 중복된 값이 없는 경우에만 INSERT 문 실행
            insert_query = "INSERT INTO menu1 (menu_id, name) VALUES (null, %s)"
            cursor.execute(insert_query, (menu,))
            conn.commit()
            cursor.close()
            conn.close()
          else:
            print("중복된 값이 있습니다.")
          print('menu', menu)
          
         
          menu_id_sql = '''
                select menu_id from menu1 where name = %s
            '''
          conn = db.getConn()
          cursor = db.getCursor()
          cursor.execute(menu_id_sql,(menu,))
          menuID = cursor.fetchone()[0]
          cursor.close()
          conn.close()
          print('name',name)
          cafeIDsql =  '''
            select id from cafe where name = %s
          '''
          conn = db.getConn()
          cursor = db.getCursor()
          cursor.execute(cafeIDsql, (name,))
          cafeID = cursor.fetchone()[0]
          cursor.close()
          conn.close()
          print(cafeID)
          query = "SELECT COUNT(*) FROM cafe_menu WHERE cafe_id = %s AND menu_id = %s"
          conn = db.getConn()
          cursor = db.getCursor()
          cursor.execute(query, (cafeID, menuID))
          count = cursor.fetchone()[0]
          cursor.close()
          conn.close()

          if count == 0:
    # 중복된 값이 없는 경우에만 INSERT 문 실행
            conn = db.getConn()
            cursor = db.getCursor()
            insert_query = "INSERT INTO cafe_menu (cafe_menu_id, cafe_id, menu_id) VALUES (null, %s, %s)"
            cursor.execute(insert_query, (cafeID, menuID))
            conn.commit()
            cursor.close()
            conn.close()
          else:
            print("중복된 값이 있습니다.")
        #   cursor.execute(sql2, (cafeID, menuID,))

          conn = db.getConn()
          cursor = db.getCursor()
          cafe_menu_IDsql =  '''
            select cafe_menu_id from cafe_menu where cafe_id = %s and menu_id = %s
          '''
          cursor.execute(cafe_menu_IDsql, (cafeID, menuID,))
          cafe_menu_id = cursor.fetchone()[0]
          cursor.close()
          conn.close()

        
    # 중복된 값이 없는 경우에만 INSERT 문 실행
          review_sql = '''
            INSERT INTO review (cafe_menu_id, review_id, taste, bean, amount, price, rate)
            VALUES (%s, null, %s, %s, %s, %s, %s)
           '''
          conn = db.getConn()
          cursor = db.getCursor()
          cursor.execute(review_sql, (cafe_menu_id, taste, been, amount, price, rate))
          conn.commit()
          cursor.close()
          conn.close()

          
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
    cursor.close()
    conn.close()

    return redirect('/registRequest')


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
    cursor.close()
    conn.close()

    print('res', res)
    l  = [list(r) for r in res]
    # for i in l:
    #     i[0] = f'[ id : {i[0]} ]'
    print(l)
    return render_template(
        'resgistRequest.html',
        l = jsonify(l).json
    )

@app.route('/reviewRequest', methods =['GET', 'POST']) # 요청 주소
def reviewRequest():
    sql =  '''
        SELECT r.review_id, c.NAME , m.name, r.taste, r.bean, r.rate, r.amount, r.price
        FROM cafe AS c
        JOIN cafe_menu AS cm
        ON c.id = cm.cafe_id
        JOIN menu1 AS m
        ON cm.menu_id = m.menu_id
        JOIN review AS r
        ON cm.cafe_menu_id = r.cafe_menu_id; 
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
        'reviewRequest.html',
        l = jsonify(l).json
    )

## cafe 
@app.route('/review/delete/<int:id>', methods =['GET']) # 요청 주소
def review_delete(id):
    sql =  '''
        delete from review
        where review_id = %s
    '''
    conn = db.getConn()
    cursor = db.getCursor()
    cursor.execute(sql, (id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/reviewRequest')


@app.route('/', methods =['GET', 'POST']) # 요청 주소
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
        cursor.close()
        conn.close()

        conn = db.getConn()
        cursor = db.getCursor()
        searchSql = '''
            select id from cafe where name = %s
        '''
        cursor.execute(searchSql,(cafeName, ))
        cafe_id = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        sql = '''
            insert into service (id,atmosphere, tableCnt, service_time,cafe_id)
            values(null, %s, %s, %s, %s)
        '''
        conn = db.getConn()
        cursor = db.getCursor()
        cursor.execute(sql,(atmo, table, time, cafe_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return render_template(
            'index.html'
        )

    else:    

        conn = db.getConn()
        cursor = db.getCursor()

        menu_top5_sql = '''
            select menu1.name, AVG(rate) from review
            join cafe_menu on review.cafe_menu_id = cafe_menu.cafe_menu_id
            join menu1 on cafe_menu.menu_id = menu1.menu_id
            group by menu1.name
            order by avg(rate) desc
            limit 5; 
        '''

        cursor.execute(menu_top5_sql)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        menuranks = [list(rows[m]) for m in range(len(rows))]
        conn = db.getConn()
        cursor = db.getCursor()
        getTop3Sql = '''
            SELECT c.name, avg(r.rate), round(avg(s.service_time),0), s.atmosphere, round(avg(s.tableCnt), 0)
            FROM cafe AS c
            JOIN cafe_menu AS cm
            ON c.id = cm.cafe_id
            JOIN menu1 AS m
            ON cm.menu_id = m.menu_id
            JOIN review AS r
            ON cm.cafe_menu_id = r.cafe_menu_id
            JOIN service as s
            ON c.id = s.cafe_id
            GROUP BY c.name
            LIMIT 3 
        '''
        cursor.execute(getTop3Sql)
        res = cursor.fetchall()
        cursor.close()
        conn.close()
        print('res', res)
        L = [[idx+1,r[0],r[2],r[3],r[4]] for idx,r in enumerate(res)]
        print('L',L)
        
        return render_template(
            'index.html', menuranks = menuranks, top3 = L
        )
         

if __name__ == '__main__':
    app.run(debug= True)