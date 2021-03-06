import re
import requests
import urllib


def clean_url(url):
    return url


def capture_urls(text):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return urls


def contain_urls(text):
    return len(capture_urls(text)) > 0


def expand_url(url):
    try:
        if 'amazon' in urllib.parse.urlparse(url).hostname:
            return url
        session = requests.Session()  # so connections are recycled
        try:
            resp = session.head(url, allow_redirects=True, timeout=10)
        except requests.exceptions.MissingSchema:
            print('----> WARNING')
            print(f'URL {url} cannot be expanded, probably this is not a valid URL, return {None}')
            return None
        return resp.url
    except Exception as e:
        print(f'Exception while expanding url: {url}\n{e}')
        return url


def get_app_name(scraper_address):
    return urllib.parse.urlparse(scraper_address).hostname.split('.')[0]


def is_aliexpress(url):
    try:
        url = expand_url(url)
    except requests.exceptions.ConnectionError:
        print(f'Exception: Connection refused {url}')
        return False
    return 'aliexpress' in urllib.parse.urlparse(url).hostname
