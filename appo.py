import os
import re
import ibm_db
from flask import Flask, session, render_template, request, redirect, send_from_directory, url_for

from helpers import login_required

app = Flask(__name__)

app.secret_key = 'password'
conn = ibm_db.connect(
    "DATABASE=bludb; HOSTNAME=2f3279a5-73d1-4859-88f0-a6c3e6b4b907.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30756; SECURITY=SSL; SSLServerCerrificate=DigiCertGlobalRootCA.crt; UID=jhk48064; PWD=pcsPf5G40FoUexOI",
    '', '')


# static file path
@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        sql = f"select * from user where name='{username}'"
        sql = ibm_db.prepare(conn, sql)
        dt = ibm_db.execute(sql)

        account = ibm_db.fetch_assoc(sql)
        # print(account)

        if account:
            session['loggedin'] = True
            # session['id'] = account['id']
            session['username'] = account['NAME']
            msg = 'Logged in successfully !'
            return redirect(url_for('products'))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/products')
def products():
    select_sql = f"select * from product;"
    select_sql = ibm_db.prepare(conn, select_sql)
    ibm_db.execute(select_sql)
    rows = []
    while True:
        data = ibm_db.fetch_assoc(select_sql)
        if not data:
            break 
        else:
            data['PRODID'] = str(data['PRODID'])
            
            rows.append(data)
    print('rows: ', rows)
    return render_template('index.html', rows=rows)


@app.route('/products/men/shirts')
def shirts():
    current_user = session["username"]
    select_sql = f"select * from product where username='divi';"
    select_sql = ibm_db.prepare(conn, select_sql)
    ibm_db.execute(select_sql)
    rows = []
    while True:
        data = ibm_db.fetch_assoc(select_sql)
        print("data:", )
        if not data:
            break
        else:
            data['PRODID'] = str(data['PRODID'])
            rows.append(data)
    print('rows: ', rows)
    return render_template("index.html", rows=rows)


@app.route('/products/men/pants')
def jeans():
    current_user = session["username"]
    select_sql = f"select * from product where username='singh';"
    select_sql = ibm_db.prepare(conn, select_sql)
    ibm_db.execute(select_sql)
    rows = []
    while True:
        data = ibm_db.fetch_assoc(select_sql)
        print("data:", )
        if not data:
            break
        else:
            data['PRODID'] = str(data['PRODID'])
            rows.append(data)
    print('rows: ', rows)
    return render_template("index.html", rows=rows)


@app.route('/products/kids')
def kids():
    current_user = session["username"]
    select_sql = f"select * from product where username='kapilan';"
    select_sql = ibm_db.prepare(conn, select_sql)
    ibm_db.execute(select_sql)
    rows = []
    while True:
        data = ibm_db.fetch_assoc(select_sql)
        print("data:", )
        if not data:
            break
        else:
            data['PRODID'] = str(data['PRODID'])
            rows.append(data)
    print('rows: ', rows)
    return render_template("index.html", rows=rows)


@app.route('/products/women/indian')
def women_indian():
    current_user = session["username"]
    select_sql = f"select * from product where username='siva';"
    select_sql = ibm_db.prepare(conn, select_sql)
    ibm_db.execute(select_sql)
    rows = []
    while True:
        data = ibm_db.fetch_assoc(select_sql)
        print("data:", )
        if not data:
            break
        else:
            data['PRODID'] = str(data['PRODID'])
            rows.append(data)
    print('rows: ', rows)
    return render_template("index.html", rows=rows)


@app.route('/products/women/western')
def women_western():
    current_user = session["username"]
    select_sql = f"select * from product where username='hari';"
    select_sql = ibm_db.prepare(conn, select_sql)
    ibm_db.execute(select_sql)
    rows = []
    while True:
        data = ibm_db.fetch_assoc(select_sql)
        print("data:", )
        if not data:
            break
        else:
            data['PRODID'] = str(data['PRODID'])
            rows.append(data)
    print('rows: ', rows)
    return render_template("index.html", rows=rows)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        sql = f"select * from user where name='{username}'"
        sql = ibm_db.prepare(conn, sql)
        dt = ibm_db.execute(sql)

        account = ibm_db.fetch_assoc(sql)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            sql = f"INSERT INTO  USER VALUES('{username}', '{email}', '{password}', 'user');"
            print(sql)
            sql = ibm_db.prepare(conn, sql)
            dt = ibm_db.execute(sql)

            msg = 'Successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        session.clear()
        username = request.form.get("username")
        password = request.form.get("password")
        sql = f"select * from admin where username='{username}'"
        sql = ibm_db.prepare(conn, sql)
        dt = ibm_db.execute(sql)

        result = ibm_db.fetch_assoc(sql)
        print("admin_login result:", result)
        # Ensure username exists and password is correct
        if result == None or result['PASSWORD'] != password:
            return render_template("error.html", message="Invalid username and/or password")
        # Remember which user has logged in
        session["username"] = result["USERNAME"]
        return redirect(url_for("home"))
    return render_template("admin_login.html")


# Admin signup
@app.route("/admin-signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        session.clear()
        password = request.form.get("password")
        repassword = request.form.get("repassword")
        if (password != repassword):
            return render_template("error.html", message="Passwords do not match!")

        fullname = request.form.get("fullname")
        username = request.form.get("username")

        sql = f"select * from admin where username='{username}'"
        sql = ibm_db.prepare(conn, sql)
        ibm_db.execute(sql)
        data = ibm_db.fetch_assoc(sql)

        if data:
            return render_template("error.html", message="Username already exists!")
        else:
            sql = f"INSERT INTO  admin VALUES('{fullname}', '{username}', '{password}');"
            sql = ibm_db.prepare(conn, sql)
            ibm_db.execute(sql)
            print("Successful Signup")
            return redirect(url_for("admin_login"))
    return render_template("admin-signup.html")


# Merchant home page to add new products
@app.route("/home", methods=["GET", "POST"], endpoint='home')
@login_required
def home():
    print("In home")
    if request.method == "POST":
        print("In post")
        image = request.files['image']
        category = request.form.get("category")
        name = request.form.get("pro_name")
        description = request.form.get("description")
        price_range = request.form.get("price_range")
        comments = request.form.get("comments")
        current_user = session["username"]
        
        columns = '"CATEGORY", "NAME","DESCRIPTION","PRICE","COMMENTS","USERNAME"'
        sql = f"INSERT INTO  PRODUCT ({columns}) VALUES('{category}', '{name}', '{description}', '{price_range}', '{comments}', '{current_user}');"
        print("Insert query", sql)
        sql = ibm_db.prepare(conn, sql)
        ibm_db.execute(sql)

        select_sql = f'select max(prodid) as maxi from product;'
        select_sql = ibm_db.prepare(conn, select_sql)
        ibm_db.execute(select_sql)
        data = ibm_db.fetch_assoc(select_sql)['MAXI']
        print("Latest product id:", data)

        filename = str(data)
        image.save(os.path.join("static/images", filename))
        current_user = session["username"]
        select_sql = f"select * from product where username='{current_user}';"
        select_sql = ibm_db.prepare(conn, select_sql)
        ibm_db.execute(select_sql)
        rows = []
        while True:
            data = ibm_db.fetch_assoc(select_sql)
            print("data:", )
            if not data:
                break
            else:
                data['PRODID'] = str(data['PRODID'])
                rows.append(data)
        print('rows: ', rows)

        return render_template("home.html", rows=rows, message="Product added")

    current_user = session["username"]
    select_sql = f"select * from product where username='{current_user}';"
    select_sql = ibm_db.prepare(conn, select_sql)
    ibm_db.execute(select_sql)
    rows = []
    while True:
        data = ibm_db.fetch_assoc(select_sql)
        if not data:
            break
        else:
            data['PRODID'] = str(data['PRODID'])
            rows.append(data)
    print('rows: ', rows)
    return render_template("home.html", rows=rows)


# When edit product option is selected this function is loaded
@app.route("/edit/<int:pro_id>", methods=["GET", "POST"], endpoint='edit')
@login_required
def edit(pro_id):
    pass


# logout
@app.route("/logout")
def admin_logout():
    session.clear()
    return redirect("/login")


if __name__ == '__main__':
    app.run(debug=True)
