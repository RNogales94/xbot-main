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
