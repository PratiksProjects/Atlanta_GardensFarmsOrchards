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
    pass

@app.route('/login', methods=['POST'])    
 def login():
    pass



