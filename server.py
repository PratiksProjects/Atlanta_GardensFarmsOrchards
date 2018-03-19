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
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    #payload = request.form
    msg = {'password':'asdf'}
    print(request)
    conn = connectDB()
    if(False):
        register_owner(conn)
    else:
        register_visitor(conn)
    return redirect('/')

def register_owner(conn, msg):
    usertype = 'Owner'
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO 'User' ('Username', 'Email', 'Password', 'UserType') VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, ('Tester','test@test.com',hash(msg['password']), usertype ))

        connection.commit()
        #add property stuff also

    finally:
        connection.close()

def register_visitor(conn, msg):
    usertype = 'Visitor'
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO 'User' ('Username', 'Email', 'Password', 'UserType') VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, ('Tester','test@test.com',hash(msg['password']), usertype ))

        connection.commit()
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
