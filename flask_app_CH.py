
from flask import Flask, request, render_template
from datetime import datetime
import pandas as pd
import csv  # for csv reader

app = Flask(__name__)


def read_csv_database():
    # Read in csv file and return it as list of rows (has header row) and

    # let's assume there's only one database with all QR codes in it as rows
    # I think you were planning to have one csv file for each code(?)
    data_folder = "./data/"
    db = data_folder + 'data_123456789.csv'

    qrprops = []
    with open(db, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            qrprops.append(row)
    return qrprops


# Load the application into the browser it will run this route the /
@app.route('/')
def dashboard():
    html_str = render_template('homepage.html' )
    return html_str

@app.route('/readqrcode/')
def readqrcode():
    html_str = render_template('qrcode.html' )
    return html_str


# Rewrote this to work with the table row as id:
#  127.0.0.1:8080/get_data_with_id/0
@app.route('/get_data_with_id/<id>')
def get_data_with_id(id):

    row = int(id) + 1

    qrprops = read_csv_database()
    props = qrprops[row]

    # Here I decided to print out the name of the property and its value ...
    props_with_names = []
    names = qrprops[0] # header row
    for i,p in enumerate(props):
        pn = names[i] + ": " + p
        props_with_names.append(pn)

    html_str = render_template('qrresults.html', id=id, props=props_with_names )
    return html_str


@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['qrcode_id']
    return 'Made it. postmethod with id: ' + jsdata

@app.route('/test_qrcode/')
def test_image():
    html_str = render_template('test.html' )
    return html_str

# testing this with 127.0.0.1:8080/qrresults/?row=0
@app.route('/qrresults/', methods=['GET'])
def display_results():

    qrprops = read_csv_database()

    # let's assume your GET gives you a way to request a specific row within your csv table
    # Maybe you were planning to use the ID and search for that row but I'm just going
    # to have a query parameter row that requests the data for that row (starting at 0!)
    row_str = request.args.get('row')
    
    # should do some checking if row is a valid string for a integer!
    row = int(row_str)

    # get data for that row (again, should check if that row id actually exists in the table!
    props = qrprops[row+1]

    html_str = render_template('qrresults.html', id=row_str, props=props)  # this only prints out the values

    return html_str




app.run(debug=False, port=8080)  # Needed to start the server locally!