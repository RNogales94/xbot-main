from scraper_proxy.proxy import Proxy

message = "https://www.amazon.es/Russell-Hobbs-20562-56-SteamGlide-Professional/dp/B00F9SUKE4/"


def test_types():
    result = Proxy().scrape(url=message)
    assert isinstance(result, list)
    assert not isinstance(result[0], list)
    assert isinstance(result[0], dict)

