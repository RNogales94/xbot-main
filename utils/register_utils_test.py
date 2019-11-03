import utils.register_utils as reg


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


