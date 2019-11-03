from utils.url_utils import capture_urls


def test_capture_urls():
    text = "/cupon ASDASD 123€ https://www.amazon.es/gp/aw/d/B06XFWF7J4/ref=ox_sc_act_image_1?smid=A1AT7YVPFBWXBL&psc=1"
    assert isinstance(capture_urls(text), list)