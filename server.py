#!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect
import sys
import pymysql.cursors
from credentials import login, temp_login

app = Flask(__name__, static_url_path="")

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
    #payload = request.form
    print(request)
    conn = connectDB()

    return redirect('/')

@app.route('/ownerRegisterPage', methods=['POST'])
def ownerRegisterPage():
    return render_template("new_owner_registration.html")

@app.route('/visitorRegisterPage', methods=['POST'])
def visitorRegisterPage():
    return render_template("new_visitor_registration.html")


@app.route('/registerOwner', methods=['POST'])
def register_owner():
    conn = connectDB()
    msg = request.form
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO User (Username, Email, Password, UserType) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (msg['username'],msg['email'],hash(msg['password']),'Owner'))

        conn.commit()
        #add property stuff also

    finally:
        conn.close()
        return redirect("/")

@app.route('/registerVisitor', methods=['POST'])
def register_visitor():
    conn = connectDB()
    msg = request.form
    password = str(hash(msg['password']))
    print(password)
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
