from flask import Flask, request
from flask import render_template
from scrape import scrape, download
import os
from time import sleep

app = Flask(__name__, static_url_path='/audio', static_folder='audio')

@app.route("/")
def index():
    url = request.args.get('url', '')
    data = None
    error = None
    if url:
        if url.startswith('http://') or url.startswith('https://'):
            try:
                data = scrape(url)
            except Exception as e:
                error = str(e)

        else:
            error = "URL should start with either http:// or https://"


    return render_template('home.html', url=url, data=data, error=error)

@app.route("/player")
def player():
    url = request.args.get('url', '')
    data = None
    error = None
    try:
        data = download(url)
    except Exception as e:
        error = str(e)
    return render_template('player.html', url=url, data=data, error=error)
