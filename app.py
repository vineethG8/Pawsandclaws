import os
import re
import ibm_db
from flask import Flask, session, render_template, request, redirect, send_from_directory, url_for
# from helpers import login_required

app = Flask(__name__)

app.secret_key = 'a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30426;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=zzp03127;PWD=KaVHuQKXQcREYtL7",'','')
print("connected")

# static file path
@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        USERNAME = request.form['username']
        PASSWORD = request.form['password']
        sql = "SELECT * FROM USER1 WHERE USERNAME=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session["USERNAME"] = account["USERNAME"]
            session['USERID'] = account['USERID']

            msg = 'Logged in successfully !'
            return redirect(url_for('pets'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('newlogin.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        USERNAME = request.form["username"]
        PASSWORD = request.form["password"]
        EMAIL = request.form["email"]
        sql = "SELECT* FROM USER1 WHERE USERNAME= ? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', EMAIL):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', USERNAME):
            msg = 'Username must contain only characters and numbers !'
        elif not USERNAME or not PASSWORD or not EMAIL:
            msg = 'Please fill out the form !'
        else:
            sql2 = "SELECT count(*) FROM USER1"
            stmt2 = ibm_db.prepare(conn, sql2)
            ibm_db.execute(stmt2)
            length = ibm_db.fetch_assoc(stmt2)
            print(length)
            sql = "INSERT INTO  USER1 VALUES(?,?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, USERNAME)
            ibm_db.bind_param(stmt, 2, EMAIL)
            ibm_db.bind_param(stmt, 3, PASSWORD)
            ibm_db.bind_param(stmt, 4, length['1']+1)
            ibm_db.execute(stmt)
            msg = 'Successfully registered!'
            print(msg)
            return render_template('newlogin.html', msg=msg)

    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('newregister.html', msg=msg)


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        # session.clear()
        USERNAME = request.form.get("username")
        PASSWORD = request.form.get("password")
        sql = "SELECT* FROM USER1 WHERE USERNAME=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        result = ibm_db.fetch_assoc(stmt)
        print(result)
        if result:
            session['Loggedin']=True
            session["USERID"]=result['USERID']
            Userid=result['USERNAME']
            session['USERNAME']=result['USERNAME']
            msg="logged in successfully !"
            return redirect(url_for('home'))
        else:
            msg="Incorrect username/password!" 
            return render_template('admin_login.html', msg=msg)
    return render_template('admin_login.html')  

# Admin signup
@app.route("/admin-signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # session.clear()
        USERNAME = request.form.get("username")
        EMAIL = request.form.get("email")
        PASSWORD = request.form.get("password")
        # password = request.form.get("password")
        sql ="SELECT * FROM USER1 WHERE USERNAME=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, USERNAME)
        ibm_db.bind_param(stmt, 2, PASSWORD)
        ibm_db.execute(stmt)
        data = ibm_db.fetch_assoc(stmt)
        if data:
            return render_template("admin-signup.html", message="Username already exists!")
        else:
            sql2 = "SELECT count(*) FROM USER1"
            stmt2 = ibm_db.prepare(conn, sql2)
            ibm_db.execute(stmt2)
            length = ibm_db.fetch_assoc(stmt2)
            print(length)
            sql = "INSERT INTO USER1 VALUES(?,?,?,?)"
            stmt = ibm_db.prepare(conn, sql)
            ibm_db.bind_param(stmt, 1, USERNAME)
            ibm_db.bind_param(stmt, 2, EMAIL)
            ibm_db.bind_param(stmt, 3, PASSWORD)
            ibm_db.bind_param(stmt, 4, length['1']+1)
            ibm_db.execute(stmt)
            # print("Successful Signup")
            print("\033[1;32m successful signup \n")
            return redirect(url_for("admin_login"))
    return render_template("admin-signup.html")


# Merchant home page to add new productss
@app.route("/home", methods=["GET", "POST"], endpoint='home')
def home():
    if request.method == "POST":
        image = request.files['image']
        PROID = request.form.get("proid")
        CATOGERY = request.form.get("category")
        SUB_CATOGERY = request.form.get("Sub-category")
        DESCRIPTION = request.form.get("description")
        PRICE_RANGE = request.form.get("price_range")
        COMMENTS = request.form.get("comments")
        # current_user = session["USERNAME"]
        sql="SELECT * FROM USER1 WHERE USERID = " +str(session['USERID']) 
        stmt=ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        data=ibm_db.fetch_tuple(stmt)
        print(data)

        insert_sql ="INSERT INTO PETS VALUES (?,?,?,?,?,?,?,?)"
        stmt1 = ibm_db.prepare(conn, insert_sql)
        ibm_db.bind_param(stmt1, 1, data[3])
        ibm_db.bind_param(stmt1, 2, PROID)
        ibm_db.bind_param(stmt1, 3, data[0])
        ibm_db.bind_param(stmt1, 4, CATOGERY)
        ibm_db.bind_param(stmt1, 5, SUB_CATOGERY)
        ibm_db.bind_param(stmt1, 6, DESCRIPTION)
        ibm_db.bind_param(stmt1, 7, PRICE_RANGE)
        ibm_db.bind_param(stmt1, 8, COMMENTS)
        ibm_db.execute(stmt1)
        print("valuessent")

        sql = 'SELECT * FROM PETS' 
        stmt2 = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt2)
        data = ibm_db.fetch_assoc(stmt2)
        print(data)
        print("Latest product id:", data)

        filename = str(data['PROID'])
        image.save(os.path.join("static/images", filename))
        # current_user = session["USERID"]
        sql = "SELECT * FROM PETS WHERE USERID=" +str(session['USERID'])
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.execute(stmt)
        data = ibm_db.fetch_assoc(stmt)
        print(data)
        rows = []
        while True:
            data = ibm_db.fetch_assoc(stmt)
            print("data:", )
            if not data:
                break
            else:
                data['PROID'] = str(data['PROID'])
                rows.append(data)
        print('rows: ', rows)
        return render_template("homen.html", rows=rows, message="Product added")

    # current_user1 = session["USERID"]
    select_sql = "SELECT * FROM PETS WHERE USERID=" +str(session['USERID'])
    stmt = ibm_db.prepare(conn, select_sql)
    ibm_db.execute(stmt)
    data = ibm_db.fetch_assoc(stmt)
    rows = []
    while True:
        data = ibm_db.fetch_assoc(stmt)
        if not data:
            break
        else:
            data['PROID'] = str(data['PROID'])
            rows.append(data)
    print('rows: ', rows)
    return render_template("homen.html", rows=rows)

@app.route('/delete_product/<string:PROID>', methods = ['POST'])
def delete_product(PROID):
    # current_user = session["USERID"]
    sql= "DELETE FROM PETS WHERE PROID=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, PROID)
    ibm_db.execute(stmt)
    # print('item deleted')
    return redirect(url_for('home'))

@app.route('/del_pro/<string:PROID>', methods = ['POST'])
def del_pro(PROID):
    # current_user = session["USERID"]
    sql= "DELETE FROM TRANSACTION WHERE PROID=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, PROID)
    ibm_db.execute(stmt)
    print('item deleted')
    return redirect(url_for('trans'))

@app.route('/add_to_cart/<string:PROID>', methods = ['GET', 'POST'])
def add_to_cart(PROID):
    # current_user = session["USERID"]
    # sql="SELECT * FROM PRODUCTS WHERE PROID ="+PROID
    sql="SELECT * FROM USER1 WHERE USERID = " +str(session['USERID']) 
    stmt=ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    data1=ibm_db.fetch_assoc(stmt)

    sql="SELECT * FROM PETS WHERE PROID ="+PROID
    stmt=ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    data=ibm_db.fetch_assoc(stmt)
    print(data)
    print('yes')
    # if request.method=='post':
    insert_sql ="INSERT INTO TRANSCATIONN VALUES (?,?,?,?,?)"
    stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(stmt, 1, data1["USERNAME"])
    ibm_db.bind_param(stmt, 2, data["PROID"])
    ibm_db.bind_param(stmt, 3, data["SUB_CATOGERY"])
    ibm_db.bind_param(stmt, 4, data["PRICE_RANGE"])
    ibm_db.bind_param(stmt, 5, data1["USERID"])
    ibm_db.execute(stmt)
    print('data sent')
    return redirect(url_for('pets'))

    # return redirect(url_for('pets'))
        # return render_template('trans.html')


@app.route('/pets')
def pets():
    sql="SELECT * FROM USER1 WHERE USERID = " +str(session['USERID']) 
    stmt=ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    data=ibm_db.fetch_assoc(stmt)
    if data['USERID']== session['USERID']:
        select_sql = "SELECT * FROM PETS"
        stmt = ibm_db.prepare(conn, select_sql)
        ibm_db.execute(stmt)
        rows = []
        while True:
            data = ibm_db.fetch_assoc(stmt)
            if not data:
                break 
            else:
                data['PROID'] = str(data['PROID'])
                rows.append(data)
        print('rows: ', rows)
        return render_template('index.html', rows=rows)

@app.route('/trans')
def trans():
    sql="SELECT * FROM USER1 WHERE USERID = " +str(session['USERID']) 
    stmt=ibm_db.prepare(conn, sql)
    ibm_db.execute(stmt)
    data=ibm_db.fetch_assoc(stmt)
    print('i am here')
    if data['USERID']== session['USERID']:
        select_sql = "SELECT * FROM TRANSCATIONN WHERE USERID="+str(session["USERID"])
        stmt = ibm_db.prepare(conn, select_sql)
        ibm_db.execute(stmt)
        data=ibm_db.fetch_tuple(stmt)
        print(data)
        rows = []
        print('i am here also')
        while data!= False:
            rows.append(data)
            data=ibm_db.fetch_tuple(stmt)
        print(rows)
        return render_template('trans.html', rows=rows)    


@app.route('/pets/doGs')
def men():
    select_sql = "SELECT * FROM PETS WHERE catogery='DOGS'"
    stmt = ibm_db.prepare(conn, select_sql)
    ibm_db.execute(stmt)
    rows = []
    while True:
        data = ibm_db.fetch_assoc(stmt)
        if not data:
            break 
        else:
            data['PROID'] = str(data['PROID'])
            rows.append(data)
    print('rows: ', rows)
    return render_template('index.html', rows=rows)

@app.route('/pets/cats')
def kids():
    # current_user = session["USERID"]
    select_sql ="SELECT * FROM PETS WHERE catogery='CATS'"
    stmt = ibm_db.prepare(conn, select_sql)
    ibm_db.execute(stmt)
    rows = []
    while True:
        data = ibm_db.fetch_assoc(stmt)
        print("data:", )
        if not data:
            break
        else:
            data['PROID'] = str(data['PROID'])
            rows.append(data)
    print('rows: ', rows)
    return render_template("index.html", rows=rows)

# @app.route('/products/womens')
# def women():
#     select_sql = "SELECT * FROM products WHERE catogery='Womens'"
#     stmt = ibm_db.prepare(conn, select_sql)
#     ibm_db.execute(stmt)
#     rows = []
#     while True:
#         data = ibm_db.fetch_assoc(stmt)
#         print("data:", )
#         if not data:
#             break
#         else:
#             data['PROID'] = str(data['PROID'])
#             rows.append(data)
#     print('rows: ', rows)
#     return render_template("index.html", rows=rows)


# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('id', None)
#     session.pop('username', None)
#     return redirect(url_for('login'))


# # When edit product option is selected this function is loaded
# @app.route("/edit/<int:pro_id>", methods=["GET", "POST"], endpoint='edit')
# # @login_required
# def edit(pro_id):
#     pass

# logout
@app.route("/logout")
def admin_logout():
    session.clear()
    return redirect("/login")


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
