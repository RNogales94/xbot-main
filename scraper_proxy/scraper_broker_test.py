from scraper_proxy.scraper_broker import ScraperBroker

broker = ScraperBroker()

def restart_scraper_test():
    status = broker.restart_scraper(broker.get_scraper())
    assert status == 202

