from urllib.request import urlopen, urlretrieve, quote
from urllib.parse import urljoin
import urllib
from bs4 import BeautifulSoup
from urllib.parse import urlparse

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

def scrape(url):
    url_info = urlparse(url)
    u = opener.open(url)
    try:
        html = u.read().decode('utf-8')
    finally:
        u.close()

    soup = BeautifulSoup(html, features="html.parser")
    results = []
    all_urls = []
    for link in soup.select('a'):
        if not link.get('href'):
            continue
        href = fix_url(link.get('href'), url_info)
        if not local_or_javacript(href):
            if is_audio_link(href):
                results.append(href)
            else:
                all_urls.append(href)
        print(href)
        #if href.startswith('javascript:'):
        #    continue
        #filename = href.rsplit('/', 1)[-1]
        #href = urljoin(url, quote(href))
        #try:
        #    urlretrieve(href, filename)
        #except:
        #    print('failed to download')
    return {
            'all': set(all_urls),
            'audio': set(results)
    }
