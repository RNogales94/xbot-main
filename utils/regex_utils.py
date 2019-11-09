import re
from utils.url_utils import capture_urls

MISSING_TAG_MESSAGE = ""
BAD_REGISTER_COMMAND = ""
REGISTER_SUCCESS = ""
OTHERL_ERROR = ""


def fix_url_if_comes_in_list(url):
    if isinstance(url, str):
        pattern = re.compile(r"^\[.*\]$")
        if pattern.match(url) is not None:
            url = url[1:]
            url = url[:-1]
            return url
    return url


def is_image_url(url):
    pattern = re.compile(r"http.*(\.jpg)|(\.png)|(\.gif)|(\.jpeg)$")
    print(pattern.match(url) is not None)
    return pattern.match(url) is not None


def is_change_tag_message(message):
    pattern = re.compile(r"^/tag(\s[\w\-]+)*$")
    print(pattern.match(message) is not None)
    return pattern.match(message) is not None


def get_amazon_tag(message):
    pattern = re.compile(r"^(/tag)\s([\w\-]+)$")
    if pattern.match(message) is not None:
        return pattern.match(message).group(2)
    else:
        return None


def get_coupon_info(message):

    pattern = re.compile(r"^/cupon\s(\w+)\s([$?\d\,\.\']+[€$]?)\s(http.*)$")
    if pattern.match(message) is not None:
        groups = pattern.match(message).groups()
        code = groups[0]
        price = groups[1]
        urls = capture_urls(groups[2])
        return {'code': code,
                'final_price': price,
                 'urls': urls}
    else:
        return None