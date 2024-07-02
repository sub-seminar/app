from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
from datetime import datetime
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # フラッシュメッセージのためのシークレットキー
session = {}
dbpath = './DATABASE.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(dbpath)
        db.execute('CREATE TABLE IF NOT EXISTS books (isbn TEXT NOT NULL, title TEXT NOT NULL, genre TEXT, author TEXT, publisher TEXT, publish_date DATE, ava_flag INTEGER DEFAULT 1, PRIMARY KEY(isbn))')
        db.execute('CREATE TABLE IF NOT EXISTS major_name (majorid INTEGER NOT NULL, majorname TEXT, PRIMARY KEY(majorid))')
        db.execute('CREATE TABLE IF NOT EXISTS rentals (rentalid INTEGER PRIMARY KEY AUTOINCREMENT, userid TEXT NOT NULL, isbn TEXT NOT NULL, rental_date DATE, return_date DATE)')
        db.execute('CREATE TABLE IF NOT EXISTS student_major (userid TEXT NOT NULL, majorid INTEGER, PRIMARY KEY(userid))')
        db.execute('CREATE TABLE IF NOT EXISTS users (userid TEXT NOT NULL, name TEXT NOT NULL, majorid TEXT,admin_flag INTEGER DEFAULT 0, PRIMARY KEY(userid))')
    return db



############################### 　ログインの処理　############################### 

# ログイン画面表示
@app.route('/')
def show_login_html(): 
    return render_template('login.html')

# ログイン画面から新規登録画面に遷移
@app.route('/register')
def show_register():
    return render_template('login_regist_user.html')

# 新規登録画面で、登録ボタンが押された際に、dbに登録し、ログイン画面に戻る処理
@app.route('/register/post', methods=['POST'])
def regist_user():
    userid = request.form['userId']
    username = request.form['username']
    major = request.form['major']
    
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('INSERT INTO users (userid, name, majorid, admin_flag) VALUES (?, ?, ?, ?)', (userid, username, major, 0))
        con.commit()
        return redirect(url_for('show_login_html'))
    except Exception as e:
        return f"登録エラー：{e}"

# ログイン画面で、adminの場合、管理者画面、一般ユーザーの場合、ユーザーホーム画面
@app.route('/login/post', methods=['POST'])
def login_process():
    userid = request.form['userId']
    
    con = get_db()
    cur = con.cursor()
    
    cur.execute('SELECT userid FROM users WHERE admin_flag = 1')
    admin_id = cur.fetchone()
    admin_id = admin_id[0] if admin_id else None
    
    cur.execute('SELECT userid FROM users WHERE admin_flag = 0')
    user_ids = cur.fetchall()
    user_ids = [user[0] for user in user_ids]
    
    if userid == admin_id:
        return redirect(url_for('show_admin_home'))
    elif userid in user_ids:
        session["userid"] = userid
        return redirect(url_for('show_user_home',user_id=userid))
    else:
        return redirect(url_for('show_login_html'))

############################### admin画面の処理 ###############################
#########admin_home画面の処理#############

# adminhome画面を表示する
@app.route('/admin_home')
def show_admin_home():
    con = get_db()
    cur = con.cursor()
    cur.execute('SELECT * FROM rentals')
    rows = cur.fetchall()
    column_names = [description[0] for description in cur.description]
    rental_list = [dict(zip(column_names, row)) for row in rows]
    con.close()

    return render_template('admin_home.html',rental_list=rental_list)

# ログアウト押されたらログイン画面に戻る
@app.route('/logout')
def logout():
    session = {}
    return redirect(url_for('show_login_html'))

# 在庫確認ボタン押された時、book_inventoryに遷移
@app.route('/admin_home/book_inventory')
def show_book_inventory():
    con = get_db()
    cur = con.cursor()
    cur.execute('SELECT * FROM books')
    rows = cur.fetchall()
    column_names = [description[0] for description in cur.description]
    book_list = [dict(zip(column_names, row)) for row in rows]
    con.close()
    return render_template('admin_check_book_inventory.html',book_list=book_list)



# ユーザー情報確認ボタンが押された時、users.htmlに遷移
@app.route('/admin_home/users')
def show_users():
    con = get_db()
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE admin_flag=0')
    rows = cur.fetchall()
    column_names = [description[0] for description in cur.description]
    user_list = [dict(zip(column_names, row)) for row in rows]
    con.close()
    return render_template('admin_check_users.html',user_list=user_list)



#########adminのbook_inventory画面#############
# 新規本登録遷移
@app.route('/admin_home/book_inventory/book_register')
def show_book_register():
    return render_template('admin_regist_book.html')

# 本登録ボタンが押された際に、その情報をdbに登録し、book_inventory.htmlの画面に戻る処理
@app.route('/admin_home/book_inventory/book_register', methods=['POST'])
def register_new_book():
    isbn = request.form['isbn']
    title = request.form['title']
    genre = request.form['genre']
    author = request.form['author']
    pub_date = request.form['pubDate']
    publisher = request.form['publisher']
    
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('INSERT INTO books (isbn, title, genre, author,publisher, publish_date, ava_flag) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                    (isbn, title, genre, author,publisher, pub_date,1))
        con.commit()
        flash('本が登録されました。', 'success')
    except Exception as e:
        flash(f'登録エラー: {e}', 'danger')

    finally:
        return redirect(url_for('show_book_inventory'))
    


@app.route('/delete_book', methods=['POST'])
def delete_book():
    data = request.get_json()
    isbn = data['isbn']
    con = get_db()
    cur = con.cursor()
    cur.execute('DELETE FROM books WHERE isbn = ?', (isbn,))
    con.commit()
    con.close()
    
    return redirect(url_for('show_book_inventory'))

#########users画面の処理#############

# 新規ユーザー登録の処理
@app.route('/admin_home/users/add', methods=['POST'])
def add_user():
    userid = request.form['userId']
    username = request.form['username']
    major = request.form['major']
    
    con = get_db()
    cur = con.cursor()
    try:
        cur.execute('INSERT INTO users (userid, name, majorid, admin_flag) VALUES (?, ?, ?, ?)', (userid, username, major, 0))
        con.commit()
        flash('ユーザーが登録されました。', 'success')
    except Exception as e:
        flash(f'登録エラー: {e}', 'danger')
    finally:
        return redirect(url_for('show_users'))


@app.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.get_json()
    userid = data['userid']

    con = get_db()
    cur = con.cursor()
    
    cur.execute('DELETE FROM users WHERE userid = ?', (userid,))
    con.commit()
    con.close()
    
    return redirect(url_for('show_users'))


############################### 一般ユーザー画面の処理 ###############################
# ユーザーホーム画面の表示
@app.route('/user_home/<user_id>')
def show_user_home(user_id):

    con = get_db()
    cur = con.cursor()
    query = 'SELECT r.rentalid, r.isbn, b.title, r.rental_date, r.return_date FROM rentals r JOIN books b ON r.isbn = b.isbn WHERE r.userid = ?'
    cur.execute(query, (user_id,))
    rows = cur.fetchall()
    column_names = [description[0] for description in cur.description]
    rental_list = [dict(zip(column_names, row)) for row in rows]
    con.close()

    return render_template('user_home.html',user_id=user_id,rental_list=rental_list)



#########ユーザーホーム画面の処理#############

# 返却申請の処理
@app.route('/return_rental', methods=['POST'])
def return_rental():
    data = request.get_json()
    rentalid = data['rentalid']
    
    con = get_db()
    cur = con.cursor()
    cur.execute('UPDATE rentals SET return_date = ? WHERE rentalid = ?', (date.today(), rentalid))
    con.commit()
    con.close()
    
    return redirect(url_for('show_user_home'))

# 本一覧ページに遷移
# @app.route('/user_home/book_list')
# def show_book_list():
#     con = get_db()
#     cur = con.cursor()
#     cur.execute('SELECT * FROM books')
#     rows = cur.fetchall()
#     column_names = [description[0] for description in cur.description]
#     book_list = [dict(zip(column_names, row)) for row in rows]
#     # con.close()

#     return_url = "/user_home/" + session["userid"]

#     cur.execute('SELECT isbn FROM rentals where return_date is NULL')
#     rows = cur.fetchall()
#     borrowed_isbns = [row[0] for row in rows]

#     con.close()

#     return render_template('users_check_books.html', book_list=book_list,return_url=return_url,borrowed_isbns=borrowed_isbns)



@app.route('/user_home/book_list', methods=['GET', 'POST'])
def show_book_list():
    search_keyword = request.form.get('searchKeyword', '')

    con = get_db()
    cur = con.cursor()
    
    if search_keyword:
        # 検索キーワードに一致する書籍を取得
        cur.execute('SELECT * FROM books WHERE title LIKE ?', ('%' + search_keyword + '%',))
    else:
        # 全書籍を取得
        cur.execute('SELECT * FROM books')
    
    rows = cur.fetchall()
    column_names = [description[0] for description in cur.description]
    book_list = [dict(zip(column_names, row)) for row in rows]

    return_url = "/user_home/" + session["userid"]

    cur.execute('SELECT isbn FROM rentals WHERE return_date IS NULL')
    rows = cur.fetchall()
    borrowed_isbns = [row[0] for row in rows]
    con.close()

    return render_template('users_check_books.html', book_list=book_list, return_url=return_url, borrowed_isbns=borrowed_isbns)










@app.route('/request_loan', methods=['POST'])
def request_loan():
    data = request.get_json()
    isbn = data['isbn']
    userid = session["userid"]
    
    con = get_db()
    cur = con.cursor()
    cur.execute('INSERT INTO rentals (userid, isbn, rental_date) VALUES (?, ?, ?)', 
                 (userid, isbn, date.today()))
    con.commit()
    con.close()
    
    return redirect(url_for('show_book_list'))


if __name__ == '__main__':
    app.run(port=5001, debug=True)
