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
    connection = sqlite3.connect("/home/flaxenink/mysite/clothes.db")
    cursor = connection.cursor()
    queryStr = "select * from qrclothes"

    cursor.execute( queryStr )
    connection.commit()
    records = cursor.fetchall()
    items = []
    for row in records:
        items.append( row)
    html_str = render_template('closet.html', items=items)
    connection.close()
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
    connection = sqlite3.connect("/home/flaxenink/mysite/clothes.db")
    cursor = connection.cursor()
    queryStr = "select * from qrclothes where id=" + id

    cursor.execute( queryStr )
    connection.commit()
    queryData = cursor.fetchone()
    result = { 'id':queryData[0], 'notes':queryData[1], 'userId':queryData[2], 'image':queryData[3], 'img_data':queryData[4], 'qrcode_data':queryData[5] }
    html_str = render_template('qrresults.html', id=id, results=result )
    connection.close()
    return html_str

@app.route('/display_qrcode/<id>')
def displayQRCode(id):
    connection = sqlite3.connect("/home/flaxenink/mysite/clothes.db")
    cursor = connection.cursor()
    queryStr = "select * from qrclothes where id=" + id

    cursor.execute( queryStr )
    connection.commit()
    queryData = cursor.fetchone()
    imgdata = queryData[4]
    qrdata = queryData[5]
    notes = queryData[1]
    html_str = render_template('display_qrcode.html', id=id, qrdata=qrdata, imgdata=imgdata, notes=notes )
    connection.close()
    return html_str

@app.route('/delete_item/<id>')
def delete_item(id):
    connection = sqlite3.connect("/home/flaxenink/mysite/clothes.db")
    cursor = connection.cursor()
    queryStr = "delete from qrclothes where id=" + id
    cursor.execute( queryStr )
    connection.commit()
    html_str = render_template('deleted_item.html', id=id )
    connection.close()
    return html_str

@app.route('/add_new_item')
def add_new_item():
    connection = sqlite3.connect("/home/flaxenink/mysite/clothes.db")
    cursor = connection.cursor()
    #cursor.execute( 'select MAX(id) from qrclothes' )
    cursor.execute('SELECT * FROM qrclothes ORDER BY id DESC LIMIT 1')

    connection.commit()
    queryData = cursor.fetchone()
    result = { 'id':queryData[0], 'notes':queryData[1] }
    html_str = render_template('additem.html', newitem=result )
    connection.close()
    return html_str

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['qrcode_id']
    return 'Made it. postmethod with id: ' + jsdata


@app.route('/save_data', methods = ['POST'])
def save_item_data():
    if request.method == 'POST':
        id = request.form.get('id')
        notes = request.form.get('notes')
        userid = request.form.get('userid')
        image = request.form.get('image')
        qrcode_data = request.form.get('qrcode_data')
        img_data = request.form.get('img_data')
        connection = sqlite3.connect("/home/flaxenink/mysite/clothes.db")
        cursor = connection.cursor()
        sqlite_insert_query = """INSERT INTO qrclothes
                          (notes, userid, image, img_data, qrcode_data)
                          VALUES (?, ?, ?, ?, ?);"""
        values = [(notes,userid,image,img_data,qrcode_data)]
        cursor.executemany(sqlite_insert_query,  values)
        connection.commit()
        html_str = render_template('save_data.html', notes=notes, id=id, qrcode_data=qrcode_data)
        connection.close()
        return html_str

@app.route('/test_qrcode/')
def test_image():
    html_str = render_template('test.html' )
    return html_str

