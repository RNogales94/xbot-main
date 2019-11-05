from utils.amazon.tools import AmazonTools

no_amazon_links = ['http://fas.st/c-oVJ', 'https://www.amazsf2234easfsafafasdfon.es/']
amazon_links = ['https://www.amazon.es/',
                'https://www.amazon.com/',
                'https://www.amazon.com/?tag=una',
                'https://amzn.to/31ftG0O']


def test_amazon_tools():
    for link in no_amazon_links:
        assert not AmazonTools.is_amazon(link)
    for link in amazon_links:
        assert AmazonTools.is_amazon(link)


def test_modify_tag():
    assert AmazonTools.modify_url('https://www.amazon.es/', 'hey-21') == 'https://www.amazon.es/?tag=hey-21'
    assert AmazonTools.modify_url('http://fas.st/c-oVJ', 'hey-21') == 'http://fas.st/c-oVJ'
    assert AmazonTools.modify_url('https://www.amazon.com/?tag=una', 'otra') == 'https://www.amazon.com/?tag=otra'
    assert AmazonTools.modify_url('https://www.amazon.com/?algo=234&tag=una', 'otra') == 'https://www.amazon.com/?algo=234&tag=otra'
