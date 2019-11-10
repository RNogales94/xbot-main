import random
import requests
import os

from utils.singleton import Singleton
from utils.url_utils import get_app_name
from scraper_proxy.config import SCRAPERS_PRO as SCRAPER_LIST


class ScraperBroker(metaclass=Singleton):
    def __init__(self):
        self.scrapers = SCRAPER_LIST
        self.current_scraper = random.choice(self.scrapers)

    def get_scraper(self, user=None):
        return self.current_scraper

    @staticmethod
    def restart_scraper(scraper_address):
        r = requests.delete(f'https://api.heroku.com/apps/{get_app_name(scraper_address)}/dynos/web.1', headers={
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.heroku+json; version=3',
        }, auth=(os.environ['HEROKU_SCRAPERS_USER'], os.environ['HEROKU_SCRAPERS_PASS']))
        print(f'Restarting {get_app_name(scraper_address)}')
        print(f'{r.content}')
        return r.status_code

    def restart_all_scrapers(self):
        for scraper in self.scrapers:
            self.restart_scraper(scraper)

    def update_current_scraper(self):
        self.restart_scraper(self.current_scraper)
        self.current_scraper = random.choice(list(set(self.scrapers) - set(self.current_scraper)))

