### Demo scraper to find audio URLs

Quick & Dirty demo.

### Development 

Requires Python 3, ideally running in a virtualenv.

```
pip install -r requirements.txt
FLASK_APP=server.py ./bin/flask run
```


### Running

```
gunicorn --bind 0.0.0.0:8000 wsgi
```
