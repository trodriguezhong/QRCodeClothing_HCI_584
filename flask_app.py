
from flask import Flask, request, render_template
import ssl
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

# This route gets all records for clothing items from sqlite and sends them to the closet template /
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

# This route gets all records for clothing items from sqlite and sends them to the closet template /
@app.route('/readqrcode/')
def readqrcode():
    html_str = render_template('qrcode.html' )
    return html_str

# This route gets a specific record according to qrid value and passes record values to display_qrcode template html/
@app.route('/get_data_with_id/<qrid>')
def get_data_with_id(qrid):
    connection = sqlite3.connect("/home/flaxenink/mysite/clothes.db")
    cursor = connection.cursor()
    queryStr = "select * from qrclothes where qrid=" + qrid

    cursor.execute( queryStr )
    connection.commit()
    queryData = cursor.fetchone()
    imgdata = queryData[4]
    qrdata = queryData[5]
    notes = queryData[1]
    html_str = render_template('display_qrcode.html', qrdata=qrdata, imgdata=imgdata, notes=notes, qrid=qrid )
    connection.close()
    return html_str

# This route gets a specific record according to qrid value and passes record values to display_qrcode template html/
@app.route('/display_qrcode/<qrid>')
def displayQRCode(qrid):
    connection = sqlite3.connect("/home/flaxenink/mysite/clothes.db")
    cursor = connection.cursor()
    queryStr = "select * from qrclothes where qrid=" + qrid

    cursor.execute( queryStr )
    connection.commit()
    queryData = cursor.fetchone()
    imgdata = queryData[4]
    qrdata = queryData[5]
    notes = queryData[1]
    html_str = render_template('display_qrcode.html', qrdata=qrdata, imgdata=imgdata, notes=notes, qrid=qrid )
    connection.close()
    return html_str

# This route receives a qrid value and deletes the associated record from the sqlite database
@app.route('/delete_item/<qrid>')
def delete_item(qrid):
    connection = sqlite3.connect("/home/flaxenink/mysite/clothes.db")
    cursor = connection.cursor()
    queryStr = "delete from qrclothes where qrid=" + qrid
    cursor.execute( queryStr )
    connection.commit()
    html_str = render_template('deleted_item.html', qrid=qrid )
    connection.close()
    return html_str

# This route gets the last qrid value and passes it to the additem.html template file
@app.route('/add_new_item')
def add_new_item():
    connection = sqlite3.connect("/home/flaxenink/mysite/clothes.db")
    cursor = connection.cursor()
    #cursor.execute( 'select MAX(id) from qrclothes' )
    cursor.execute('SELECT * FROM qrclothes ORDER BY qrid DESC LIMIT 1')

    connection.commit()
    queryData = cursor.fetchone()
    #result = { 'id':queryData[0], 'notes':queryData[1] }
    notes = queryData[1]
    id = queryData[0]
    qrid = queryData[6]
    html_str = render_template('additem.html', id=id, qrid=qrid)
    connection.close()
    return html_str

# This route gets POST data from the browser with new item information.
#  It then insterts the new item record into the database.  Returns a save_data view
@app.route('/save_data', methods = ['POST'])
def save_item_data():
    if request.method == 'POST':
        qrid = request.form.get('id')
        notes = request.form.get('notes')
        userid = request.form.get('userid')
        image = request.form.get('image')
        qrcode_data = request.form.get('qrcode_data')
        img_data = request.form.get('img_data')
        connection = sqlite3.connect("/home/flaxenink/mysite/clothes.db")
        cursor = connection.cursor()
        sqlite_insert_query = """INSERT INTO qrclothes
                          (notes, userid, image, img_data, qrcode_data, qrid)
                          VALUES (?, ?, ?, ?, ?, ?);"""
        values = [(notes,userid,image,img_data,qrcode_data, qrid)]
        cursor.executemany(sqlite_insert_query,  values)
        connection.commit()
        html_str = render_template('save_data.html', notes=notes, qrcode_data=qrcode_data, qrid=qrid)
        connection.close()
        return html_str


