import json
from flask import Flask, request, Response
from flask_cors import CORS
from utils.url_utils import is_aliexpress, captureURLs
from xbot.xbotdb import Xbotdb
from xbot.utils.product import load_product_from_json

from utils.amazon.tools import AmazonTools

from scraper_proxy.proxy import Proxy

xbot_webservice = Flask(__name__)
CORS(xbot_webservice)

proxy = Proxy()
xbotdb = Xbotdb()


@xbot_webservice.route("/")
def index():
    return 'xbot_proxy'


@xbot_webservice.route('/api/scrape', methods=['POST'])
def redirect_scrape():
    print('-------------------------------------------')
    url = request.json.get('url')
    user = request.json.get('user') or None
    print('URL='+url)
    print('user='+user)
    if AmazonTools.is_amazon(url) or is_aliexpress(url):
        scraped = proxy.scrape(url, user)
        response = json.dumps(scraped['data'])
        status = scraped['status']
    else:
        response = {}
        status = 400
    print('***********************************************')
    return Response(response, status=status, mimetype='application/json')


@xbot_webservice.route('/api/newoffer', methods=['POST'])
def new_offer():
    if request.content_type != 'application/json':
        return Response(json.dumps({'Error': 'Content-Type must be application/json'}), status=400, mimetype='application/json')

    payload = request.json
    message = payload.get('message')
    origin = payload.get('origin')

    if message is None:
        error_message = '"message" field is mandatory, try with {"message": "hello world", "origin": "me"}'
        return Response(json.dumps({'Error': error_message}), status=400, mimetype='application/json')

    urls = captureURLs(message)
    offers = []
    for url in urls:
        print(url)
        if AmazonTools.is_amazon(url) or is_aliexpress(url):
            scraped = proxy.scrape(url, 'XBOT_API')
            status = scraped['status']
        else:
            status = 400

        if status == 200:
            offers.append(scraped['data'])
        print(origin)

    for offer in offers:
        # Save in Mongo
        product = load_product_from_json(offer)
        if product.is_completed:
            xbotdb.insert_product(product, telegram_name='XBOT_API')
    print({'Message': f'Document inserted in mongo ({len(offers)})'})
    return Response(json.dumps(offers), status=200, mimetype='application/json')


@xbot_webservice.route('/api/todayamazon')
def get_todays_offers_from_amazon():
    pass

