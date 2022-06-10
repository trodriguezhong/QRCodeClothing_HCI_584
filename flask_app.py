import feedparser
from flask import Flask, request, render_template
import ssl
from datetime import datetime

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

@app.route('/qrresults/', methods=['POST', 'GET'])
def display_results():
    if request.method == 'GET':
        data = request.args.get('q')
        qrcode_id = data

    headings = []
    qrprops = []
    row_index = 0
    with open('../static/data/data_123456789.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row_index == 0:
                headings.append( row )
            else:
                qrprops.append( row )
        row_index += 1

    html_str = render_template('qrresults.html', headings=headings, props=qrprops, id=qrcode_id )
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
