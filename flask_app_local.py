import feedparser
from flask import Flask, request, render_template
import ssl
from datetime import datetime
import pandas as pd
import os
import sqlite3
import logging

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

# Load the application into the browser it will run this route the /
@app.route('/')
def dashboard():
    html_str = render_template('homepage.html' )
    return html_str

@app.route('/closet')
def closet():
    html_str = render_template('closet.html' )
    return html_str

@app.route('/settings')
def settings():
    html_str = render_template('settings.html' )
    return html_str

@app.route('/readqrcode/')
def readqrcode():
    html_str = render_template('qrcode.html' )
    return html_str

@app.route('/get_data_with_id/<id>')
def get_data_with_id(id):
    connection = sqlite3.connect("clothes.db")
    cursor = connection.cursor()
    queryStr = "select * from qrclothes where id=" + id

    cursor.execute( queryStr )
    connection.commit()
    queryData = cursor.fetchone()
    result = { 'id':queryData[0], 'notes':queryData[1], 'userId':queryData[2], 'image':queryData[3] }
    html_str = render_template('qrresults.html', id=id, results=result )
    connection.close()
    return html_str

@app.route('/add_new_item')
def add_new_item():
    connection = sqlite3.connect("clothes.db")
    cursor = connection.cursor()
    cursor.execute( 'select MAX(id) from qrclothes' )
    connection.commit()
    nextID = cursor.fetchone()  # (1234568, ) which is a tuple with 1 element
    nextID = nextID[0] # unpack tuple
    html_str = render_template('additem.html', newitem=nextID )
    connection.close()
    return html_str

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['qrcode_id']
    return 'Made it. postmethod with id: ' + jsdata

@app.route('/test_qrcode/')
def test_image():
    html_str = render_template('test.html' )
    return html_str

# Run app locally
app.run(debug=False, port=8080)
