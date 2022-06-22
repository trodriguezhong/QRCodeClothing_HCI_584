import feedparser
from flask import Flask, request, render_template
import ssl
from datetime import datetime
import pandas as pd
import os
import mysql.connector


if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

FEED_URL = "https://news.google.com/rss"

#db = MySQLdb.connect("flaxenink.mysql.pythonanywhere-services.com", "flaxenink", "2038Test**", "flaxenink")


# Load the application into the browser it will run this route the /
@app.route('/')
def dashboard():
    html_str = render_template('homepage.html' )
    return html_str

@app.route('/readqrcode/')
def readqrcode():
    html_str = render_template('qrcode.html' )
    return html_str

@app.route('/get_data_with_id/<id>')
def get_data_with_id(id):
    #cnx = mysql.connector.connect(user='<username>', password='<passsword>', host='flaxenink.mysql.pythonanywhere-services.com', database='<username>$default')
    #cnx = mysql.connector.connect(user='flaxenink', database='default', host='flaxenink.mysql.pythonanywhere-services.com')

    cnx = mysql.connector.connect(
        host='flaxenink.mysql.pythonanywhere-services.com',
        user='flaxenink',
        passwd='cl0th1ng1nf04ALL',
        database='flaxenink$default',
        pool_name='poolname',
        pool_size=20,
        connection_timeout=300,
        #auth_plugin='mysql_native_password'
    )

    cursor = cnx.cursor()



    clothesData = []
    qrcodeId = '1234567'
    #results = ["hog", "fish", "hippo"]
    query = ("SELECT * FROM clothes WHERE id=%s")
    cursor.execute(query, qrcodeId )


    for (notes, userId, image) in cursor:
        clothesData.append( notes, userId, image )

    html_str = render_template('qrresults.html', id=qrcodeId, results=clothesData )

    cursor.close()
    cnx.close()

    return html_str


@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['qrcode_id']
    return 'Made it. postmethod with id: ' + jsdata

@app.route('/test_qrcode/')
def test_image():
    html_str = render_template('test.html' )
    return html_str
