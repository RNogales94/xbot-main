import re

MISSING_TAG_MESSAGE = ""
BAD_REGISTER_COMMAND = ""
REGISTER_SUCCESS = ""
OTHERL_ERROR = ""


def is_register_message(message):
    pattern = re.compile(r"^/register(\s[\w\-]+)*$")
    print(pattern.match(message) is not None)
    return pattern.match(message) is not None


