from scraper_proxy.proxy import Proxy
import requests

message = "https://www.amazon.es/Russell-Hobbs-20562-56-SteamGlide-Professional/dp/B00F9SUKE4/"


# def test_fixture(requests_mock):
#     requests_mock.get("http://123-fake-api.com", text="Hello!")
#     response = requests.get("http://123-fake-api.com")
#
#     assert response.text == "Hello!"


# def test_types():
#     result = Proxy().scrape(url=message)
#     assert isinstance(result, list)
#     assert not isinstance(result[0], list)
#     assert isinstance(result[0], dict)
#

bad_url = 'http://www.google.com'
responses = Proxy().scrape_single_url(bad_url)

url = 'https://www.amazon.es/Russell-Hobbs-20562-56-SteamGlide-Professional/dp/B00F9SUKE4/'
responses = Proxy().scrape(url)


def scrape_single_url():
    pass





def test_scrape_proxy():
    url = []
    responses = Proxy().scrape(url)
    assert isinstance(responses, list)
    for item in responses:
        data = item['data']
        status = item['status']
        assert status == 200
        assert isinstance(data, dict)
        assert 'short_description' in data.keys()
        assert 'description' in data.keys()
        assert 'features' in data.keys()
        assert 'standard_price' in data.keys()
        assert 'end_date' in data.keys()
        assert 'price' in data.keys()
        assert 'url' in data.keys()
        assert 'image_url' in data.keys()
        assert 'size' in data.keys()
        assert 'is_captcha' in data.keys()


def test_scrape_proxy():
    url = 'https://www.amazon.es/Russell-Hobbs-20562-56-SteamGlide-Professional/dp/B00F9SUKE4/'
    responses = Proxy().scrape(url)
    assert isinstance(responses, list)
    for item in responses:
        data = item['data']
        status = item['status']
        assert status == 200
        assert isinstance(data, dict)
        assert 'short_description' in data.keys()
        assert 'description' in data.keys()
        assert 'features' in data.keys()
        assert 'standard_price' in data.keys()
        assert 'end_date' in data.keys()
        assert 'price' in data.keys()
        assert 'url' in data.keys()
        assert 'image_url' in data.keys()
        assert 'size' in data.keys()
        assert 'is_captcha' in data.keys()




