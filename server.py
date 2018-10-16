from flask import Flask, request
from flask import render_template
from scrape import scrape

app = Flask(__name__)

@app.route("/")
def hello():
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

@app.route("/", methods=["POST"])
def extract():
    return "Hello World2!"
