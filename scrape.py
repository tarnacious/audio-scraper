from urllib.request import urlopen, urlretrieve, quote
from urllib.parse import urljoin
import urllib
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import fleep
import tempfile
import shutil
import os.path
import hashlib

url = 'https://alternativlos.org/35'
#url = 'https://www.thisamericanlife.org/489/no-coincidence-no-story'

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()

def is_audio_link(url):
    if not url:
        return False
    if url.endswith(".mp3"):
        return True
    if url.endswith(".ogg"):
        return True
    if url.endswith(".opus"):
        return True
    if url.endswith(".wav"):
        return True
    if url.endswith(".acc"):
        return True
    return False

def local_or_javacript(url):
    if url.startswith("javascript"):
        return True
    if url.startswith("#"):
        return True
    return False

def fix_url(url, url_info):
    url = url.strip()
    if url.startswith("//"):
        return url_info.scheme + ":" + url
    if url.startswith("/"):
        return url_info.scheme + "://" + url_info.netloc + url
    return url

def find_feeds(soup):
    rss_links = soup.select('link', type='application/rss+xml')
    print(rss_links)
    return []


def find_urls(soup, base_url):
    url_info = urlparse(base_url)
    for link in soup.select('a'):
        if link.get('href'):
            href = fix_url(link.get('href'), url_info)
            if not local_or_javacript(href):
                yield href


def alternate_links(soup, base_url):
    feed_types = [
        'application/rss+xml',
        'application/atom+xml'
    ]
    url_info = urlparse(base_url)
    feed_urls = soup.findAll("link", rel="alternate")
    result = []
    for feed_link in feed_urls:
        url = feed_link.get("href", None)
        if url:
            feed_type = feed_link.get("type", "").lower()
            if feed_type in feed_types:
                result.append({
                    'type': feed_link.get("type", ""),
                    'title': feed_link.get("title", ""),
                    'url': fix_url(url, url_info)
                })
    return result


def scrape(url):
    url_info = urlparse(url)
    u = opener.open(url)
    try:
        html = u.read().decode('utf-8')
    finally:
        u.close()

    soup = BeautifulSoup(html, features="html.parser")
    urls = list(find_urls(soup, url))
    results = list(filter(is_audio_link, urls))
    all_urls = set(urls) - set(results)
    links = alternate_links(soup, url)

    return {
        'all': set(all_urls),
        'audio': set(results),
        'feeds': links
    }


def download(url):
    try:
        os.makedirs("audio")
    except FileExistsError:
        pass
    filename = "audio/" + hashlib.sha1(url.encode('utf-8')).hexdigest()
    if not os.path.isfile(filename):
        tmpfile = tempfile.mktemp()
        opener.retrieve(url, tmpfile)
        shutil.move(tmpfile, filename)
    with open(filename, "rb") as file:
        info = fleep.get(file.read(128))
    filesize = os.path.getsize(filename)
    return {
        'path': filename,
        'size': filesize,
        'extension': info.extension,
        'mime': next(iter(info.mime), None)
    }

if __name__ == "__main__":
    #print(scrape("https://alternativlos.org/35"))
    print(scrape("https://tarnbarford.net"))
