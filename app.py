#made by Team Ganador

import json
from flask import Flask, redirect, request, render_template, jsonify
from youtube_transcriber import search_keywords
from sum.py import fun
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/sum.py')
def summariser():
    fun()
    yield('hi')

@app.route('/search_keyword', methods=['POST'])
def searchKeyWord():

    url = request.form["url"]
    keyword = request.form["keyword"]
    result = search_keywords(url, keyword)

    if not result:
        return jsonify(dict())

    return jsonify(timeStamp(result))


def timeStamp(list_time):
 
    format_time = dict()
    i = 0
    for time in list_time:
        m, s = divmod(time, 60)
        h, m = divmod(m, 60)
        format_time[str(i)] = {"%dh%02dm%02ds" % (h, m, s): time}
        i += 1
    return format_time


if __name__ == '__main__':
    app.run()
