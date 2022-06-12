import feedparser
from flask import Flask, request, render_template
import ssl
from datetime import datetime
import pandas as pd
import os

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

FEED_URL = "https://news.google.com/rss"

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
    csvfilename = "../static/data/data_123456789.csv"
	# to read the csv file using the pandas library
    props = ["hog", "fish", "hippo"]

    html_str = render_template('qrresults.html', id=id, props=props )
    return html_str


@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    jsdata = request.form['qrcode_id']
    return 'Made it. postmethod with id: ' + jsdata

@app.route('/test_qrcode/')
def test_image():
    html_str = render_template('test.html' )
    return html_str

@app.route('/qrresults/', methods=['POST', 'GET'])
def display_results():
    searchstr = "";

#csv reader
    this_folder = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(this_folder, 'data_123456789.csv')
    qrprops = []
    row_index = 0
    with open(my_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            qrprops.append( row )
        row_index += 1
#end csv reader

    if request.method == 'GET':
        data = request.args.get('q')
        data.strip()

    dataarr = data.split(' ')
    if len( dataarr ) > 1:
        searchstr = '+'.join(dataarr)
    else:
        searchstr = data

    html_str = render_template('qrresults.html', id=searchstr, props=props )
    return html_str


@app.route('/result/', methods=['POST', 'GET'])
def search():
    if request.method == 'GET':
        data = request.args.get('q')
        data.strip()

    dataarr = data.split(' ')
    if len( dataarr ) > 1:
        searchstr = '+'.join(dataarr)
    else:
        searchstr = data

    posts = []
    searchterm = FEED_URL + "?q=" + searchstr
    print("searchterm is", searchterm )
    feed = feedparser.parse( searchterm ) # Atom + RSS
    for entry in feed["entries"]:
        title = entry.get("title")
        link = entry.get("link")
        pubdate = entry.published

        posts.append( {"title":title, "link":link, "pubdate":pubdate })

    html_str = render_template('results.html', posts=posts, searchterm=data )
    return html_str
