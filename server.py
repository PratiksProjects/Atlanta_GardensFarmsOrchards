#!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect
import sys
import pymysql.cursors
from credentials import temp_login
from random import randint
import hashlib

app = Flask(__name__, static_url_path="")

profile_pages = {"Admin":"admin.html","Visitor":"visitor.html","Owner":"owner.html"}

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def yesno_to_bool(str):
    if(str.lower() == "yes"):
        return 1
    else:
        return 0

def connectDB():
    connection = pymysql.connect(host= temp_login['SERVER_ADDRESS'],
                                 user= temp_login['USERNAME'],
                                 password= temp_login['PASSWORD'],
                                 db= temp_login['DB'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

@app.route('/', methods=['GET'])
def home():
    #return render_template('login_new.html')
    return render_template('login_new.html')

@app.route('/login', methods=['POST'])
def login():
    msg = request.form
    h= hashlib.md5()
    sql = "SELECT * from User WHERE Username = %s"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql, (msg['username'],))
        results = cur.fetchone()

    conn.close()
    if(results not None):
        if(str(results['Password']) ==  str(h.update(msg['password']))):
            ##change to profile pages once done
            user_type = results['UserType']
            resp = make_response(redirect("/"+ user_type))
            resp.set_cookie('type', user_type)
            return resp
    else:
        return redirect("/")

@app.route('/Visitor', methods=['GET'])
def visitor_profile():
    print(request.cookies)
    if(request.cookies.get('type') == 'Visitor'):
        return render_template("visitor.html")
    else:
        return redirect('/')

@app.route('/Owner', methods=['GET'])
def owner_profile():
    if(request.cookies.get('type') == 'Owner'):
        return render_template("owner.html")
    else:
        return redirect('/')

@app.route('/Admin', methods=['GET'])
def admin_profile():
    if(request.cookies.get('type') == 'Admin'):
        return render_template("admin_functionality.html")
    else:
        return redirect('/')

@app.route('/ownerRegisterPage', methods=['POST'])
def owner_register_page():
    return render_template("new_owner_registration.html")

@app.route('/visitorRegisterPage', methods=['POST'])
def visitor_register_page():
    return render_template("new_visitor_registration.html")

@app.route('/registerOwner', methods=['POST'])
def register_owner():
    conn = connectDB()
    h = hashlib.md5()
    msg = request.form
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO User (Username, Email, Password, UserType) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (msg['username'],msg['email'],h.update(msg['password']),'Owner'))

        conn.commit()
        isPublic = yesno_to_bool(msg['isPublic'])
        isCommercial = yesno_to_bool(msg['isCommercial'])
        with conn.cursor() as cur:
            sql = "INSERT INTO Property (ID, Name, Size, Street, City, Zip, IsPublic, IsCommercial, PropertyType, Owner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (random_with_N_digits(5), msg['propertyName'], int(msg['acres']),msg['streetAddress'],msg['city'], msg['zip'], isPublic, isCommercial, msg['propertyType'], msg['username']))

        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return redirect("/")

@app.route('/registerVisitor', methods=['POST'])
def register_visitor():
    h = hashlib.md5()
    conn = connectDB()
    msg = request.form
    password = str(h.update(msg['password']))
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO User (Username, Email, Password, UserType) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (msg['username'],msg['email'],password,'Visitor'))

        conn.commit()

    except Exception as e:
        print(e)
    finally:
        conn.close()
        return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
