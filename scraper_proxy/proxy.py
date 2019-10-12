import requests

from utils.singleton import Singleton
from scraper_proxy.scraper_broker import ScraperBroker
from scraper_proxy.config import baned_users
from scraper_proxy.config import SCRAPER_ENDPOINT


@Singleton
class Proxy:
    def __init__(self):
        self.scrape_broker = ScraperBroker()

    def scrape(self, url, user):
        scraper = self.scrape_broker.get_scraper(user)

        print(f'Using {scraper}')

        if user in baned_users:
            return {'data': {'Error': 'Has agotado tu periodo de prueba, contacta con @RNogales para renovarlo'}, 'status': 200}

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
                self.scrape_broker.update_current_scraper(user)
                r = requests.post(f'{scraper}{SCRAPER_ENDPOINT}', json={'url': url})

            return {'data': r.json(), 'status': 200}
