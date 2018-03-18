#!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect
import sys
import pymysql

app = Flask(__name__, static_url_path="")

def connectDB():
    connection = pymysql.connect(host='localhost',
                                 user='user',
                                 password='passwd',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

@app.route('/', methods=['GET'])
def home():
    conn = sqlite3.connect('ece4813-lab3-college.sqlite')
    results = conn.execute("SELECT * FROM student;");
    
    studentlist=[]
    for item in results:
        student={}
        student['ID'] = item[0]
        student['Name'] = item[1]
        student['LastName'] = item[2]
        studentlist.append(student)
    
    conn.close()        
    return render_template('index.html', students=studentlist)

@app.route('/login', methods=['POST'])    
 def login():
    pass



