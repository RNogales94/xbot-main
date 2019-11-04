from bot_handler.line_formater import LineFormater
from lxml import etree
from io import StringIO


def validate_html(html):
    html_parser = etree.HTMLParser(recover=False)
    try:
        node = etree.parse(StringIO(html), html_parser)
        return len(node.parser.error_log) == 0
    except Exception as e:
        print(f'HTML ERROR ---> \n\t{e}')
        return False


def test_get_image_url_line():
    assert isinstance(LineFormater.get_image_url_line('asdasd'), str)
    assert validate_html(LineFormater.get_image_url_line('https://pypi.org/project/py_w3c/'))
    assert validate_html(f'<a href="https://pypi.org/project/py_w3c/">nothing </a>')
    assert not validate_html(f'<a href="https://pypi.org/project/py_w3c/">nothing </a')


def test_get_title_line():
    assert isinstance(LineFormater.get_title_line('Mi titulo'), str)
    assert isinstance(LineFormater.get_title_line('Mi titulo', 'default'), str)
    assert isinstance(LineFormater.get_title_line(title='Mi titulo', style='default'), str)
    assert isinstance(LineFormater.get_title_line(title='Mi titulo', style='uno que no hay'), str)
    assert validate_html(LineFormater.get_title_line(title='Mi titulo', style='uno que no hay'))
    assert LineFormater.get_title_line("Mi titulo", "mal style") == LineFormater.get_title_line("Mi titulo", "default")


def test_get_description_line():
    assert isinstance(LineFormater.get_description_line('Desc'), str)


def test_get_size_line():
    assert isinstance(LineFormater.get_size_line('234'), str)
    assert isinstance(LineFormater.get_size_line('234', 'Vincent_Vegaa'), str)

