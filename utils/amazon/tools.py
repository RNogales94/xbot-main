import re
import requests
import random
import os
import urllib

from utils.url_utils import expand_url

GAIN_RATE = 0.0  # Lower is better for xbot owner


class AmazonTools:
    @classmethod
    def is_amazon(cls, url):
        try:
            url = expand_url(url)
        except requests.exceptions.ConnectionError:
            print(f'Exception: Connection refused {url}')
            return False
        return 'amazon' in urllib.parse.urlparse(url).hostname

    @classmethod
    def modify_url(cls, url, tag, is_user_free=False):
        if cls.is_amazon(url):
            if is_user_free and random.random() > GAIN_RATE:
                tag = os.environ["XBOT_AMAZON_TAG"] or tag
            url = expand_url(url)
            tag_pattern = r'tag=[^&]+'

            if re.search(tag_pattern, url):
                url = re.sub(tag_pattern, 'tag=' + tag, url)
            else:
                if '?' in url:
                    url = url + '&tag=' + tag
                else:
                    url = url + '?tag=' + tag
            return url
        else:
            return url


