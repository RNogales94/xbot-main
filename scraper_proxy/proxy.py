import requests
import random
from utils.singleton import Singleton
from scraper_proxy.scraper_broker import ScraperBroker
from scraper_proxy.config import SCRAPER_ENDPOINT


class Proxy(metaclass=Singleton):
    def __init__(self):
        self.scrape_broker = ScraperBroker()

    def __get_scraper_response(self, url):
        scraper = self.scrape_broker.get_scraper(user=None)
        print(f'Using {scraper}')

        r = requests.post(f'{scraper}{SCRAPER_ENDPOINT}', json={'url': url})
        status = r.status_code
        if status == 503:
            data = {'Error': 'Amazon CAPTCHA'}
        else:
            data = r.json()

        print(f"[Proxy] Scraper {scraper} return status {status}...")
        print(f"[Proxy] scraper {scraper} returned:\n{data}")

        return data, status

    @staticmethod
    def should_restart_scraper(data, status):
        if status == 503:
            print("[Proxy] Restarting due to CAPTCHA...")
            return True
        elif 'Error' in data.keys() and status < 400:
            print("[Proxy] Restarting due to ERROR with status < 200...")
            return True
        else:
            if random.random() < 0.1:
                return True
            print('[Proxy] No restart scraper')
            return False

    def scrape_single_url(self, url):

        data, status = self.__get_scraper_response(url=url)

        if self.should_restart_scraper(data, status):  # Restart this broker if it's broken or banned
            self.scrape_broker.update_current_scraper()
            data, status = self.__get_scraper_response(url=url)

        return {'data': data, 'status': status}

    def scrape(self, url):
        """
        Scrape urls and get information for a url

        :param url: Single url or url list
        :param user_type: (optional) user type valid values "PRO" "BOT" "STANDARD"
        :return: A list of JSON with all the features extracted for each url
        """
        if isinstance(url, list):
            urls = url
            result = [self.scrape_single_url(url) for url in urls]
        if isinstance(url, str):
            result = [self.scrape_single_url(url)]

        return result
