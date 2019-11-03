import re

MISSING_TAG_MESSAGE = ""
BAD_REGISTER_COMMAND = ""
REGISTER_SUCCESS = ""
OTHERL_ERROR = ""


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
