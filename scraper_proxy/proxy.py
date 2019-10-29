import requests

from utils.singleton import Singleton
from scraper_proxy.scraper_broker import ScraperBroker
from scraper_proxy.config import baned_users
from scraper_proxy.config import SCRAPER_ENDPOINT


@Singleton
class Proxy:
    def __init__(self):
        self.scrape_broker = ScraperBroker()

    def __scrape(self, url):
        scraper = self.scrape_broker.get_scraper(user=None)

        print(f'Using {scraper}')

        if url == '':
            return {'data': {'Error': 'Parameter url not found'}, 'status': 400}
        else:
            r = requests.post(f'{scraper}{SCRAPER_ENDPOINT}', json={'url': url})
            print(r.status_code)
            try:
                data = r.json()
                print(data)
            except:
                print(f"Scraper {scraper} cannot scrape {url}")
                return {'data': {}, 'status': 501}

            if r.json().get('short_description') is None:
                self.scrape_broker.update_current_scraper(user=None)
                r = requests.post(f'{scraper}{SCRAPER_ENDPOINT}', json={'url': url})

            return {'data': r.json(), 'status': 200}

    def scrape(self, url, user_type=None):
        """
        Scrape urls and get information for a url

        :param url: Single url or url list
        :param user_type: (optional) user type valid values "PRO" "BOT" "STANDARD"
        :return: A list of JSON with all the features extracted for each url
        """
        if type(url) == type(list()):
            urls = url
            result = [self.__scrape(url) for url in urls]
        if type(url) == type('string'):
            result = [self.__scrape(url)]

        return result
