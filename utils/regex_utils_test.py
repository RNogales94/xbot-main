import utils.regex_utils as reg


def test_is_change_tag_message():
    assert reg.is_change_tag_message('/tag mitag')
    assert reg.is_change_tag_message('/tag')
    assert reg.is_change_tag_message('/tag unatag-21 mas cosas')
    assert not reg.is_change_tag_message('tag unatag-21')
    assert not reg.is_change_tag_message('/tg mitag-21')


def test_get_amazon_tag():
    assert reg.get_amazon_tag('/tag mitag-21') == 'mitag-21'
    assert reg.get_amazon_tag('/tag mitag-21 mas cosas') is None
    assert reg.get_amazon_tag('/tg') is None
    assert reg.get_amazon_tag('/tag') is None
    assert reg.get_amazon_tag('/tag ') is None
    assert reg.get_amazon_tag('/tag 213') == '213'


def test_get_cupon_info():
    assert reg.get_coupon_info('/cupon') is None
    assert reg.get_coupon_info('/cupon 10€') is None
    assert reg.get_coupon_info('/cupon 23423ASD 50€') is None
    assert reg.get_coupon_info('/cupon 23423ASD 50€ http://google.com') is not None
    assert reg.get_coupon_info('/cupon 23423ASD 50€ http://google.com')['code'] == "23423ASD"
    assert reg.get_coupon_info('/cupon 23423ASD 50€ http://google.com')['final_price'] == "50€"
    assert reg.get_coupon_info('/cupon 23423ASD 50€ http://google.com')['link'] == "http://google.com"
    assert reg.get_coupon_info('/cupon 23423ASD 50€ http://google.com mas cosas')['link'] == "http://google.com"
    complex_url = "https://www.google.com/search?q=regex101&oq=regex&aqs=chrome.2.69j0l3.2837&sourceid=chrome&ie=UTF-8"
    assert reg.get_coupon_info(f'/cupon 23423ASD 50€ {complex_url}')['link'] == complex_url




