import json
from flask import Flask, request, Response
from flask_cors import CORS
from utils.url_utils import is_aliexpress, capture_urls
from xbot.xbotdb import Xbotdb
from xbot.utils.product_factory import ProductFactory
from bot_handler.telegram_config import BOT_URL
from bot_handler.bot import Bot
import requests
from utils.amazon.tools import AmazonTools
from datetime import datetime

from scraper_proxy.proxy import Proxy
import os

xbot_webservice = Flask(__name__)
CORS(xbot_webservice)

proxy = Proxy()
xbotdb = Xbotdb()

bot = Bot()


# [213337828, 9623929, 24843237]]:
#  [213337828, 24843237]]:


@xbot_webservice.route("/")
def index():
    return 'xbot_proxy'


@xbot_webservice.route('/api/scrape', methods=['POST'])
def redirect_scrape():
    if request.headers.get('Content-Type') != 'application/json':
        error_message = json.dumps({'Error': 'Content-Type must be application/json'})
        return Response(error_message, status=400, mimetype='application/json')
    url = request.json.get('url')
    user = request.json.get('user') or None

    if url is None:
        error_message = json.dumps({'Error': 'Must send a url in the json body'})
        return Response(error_message, status=400, mimetype='application/json')

    if user is None:
        print("Warning: Request come from user None")

    if AmazonTools.is_amazon(url) or is_aliexpress(url):
        scraped = proxy.scrape(url, user)
        response = json.dumps(scraped['data'])
        status = scraped['status']
    else:
        response = json.dumps({'Error': 'No valid Amazon URL / AliExpress URL'})
        status = 400

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

    urls = capture_urls(message)
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
        product = ProductFactory.build_product_from_json(offer)
        if product.is_completed:
            xbotdb.insert_product(product, telegram_name='XBOT_API')
    print({'Message': f'Document inserted in mongo ({len(offers)})'})
    return Response(json.dumps(offers), status=200, mimetype='application/json')


@xbot_webservice.route('/api/todayamazon', methods=['POST'])
def get_todays_offers_from_amazon():

    if request.content_type != 'application/json':
        return Response(json.dumps({'Error': 'Content-Type must be application/json'}), status=400, mimetype='application/json')
    request_data = request.json
    print(request_data)

    good_products_counter = 0
    for item in request_data:
        data = item['data']
        if 'Error' not in data.keys() and data['short_description'] is not None:
            good_products_counter = good_products_counter + 1
            for chat_id, user in [(id, xbotdb.get_user_by_chat_id(id)) for id in [213337828]]:
                message = bot.build_message_from_json(data, user)
                if message != 'None':
                    # Send message
                    json_data = {
                        "chat_id": chat_id,
                        "text": message,
                        'parse_mode': 'HTML'
                    }
                    message_url = BOT_URL + 'sendMessage'
                    requests.post(message_url, json=json_data)

    now = datetime.now().strftime("[%A] %m/%d/%Y, %H:%M:%S")
    counters = f"{good_products_counter}/{len(request_data)}"
    json_data = {
        "chat_id": 213337828,
        "text": f'Fin de los productos de hoy {now}\nTotal de hoy {counters} productos',
        'parse_mode': 'HTML'
    }
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=json_data)

    return Response(json.dumps({'Success': 'True'}), status=200, mimetype='application/json')


@xbot_webservice.route('/bot', methods=['POST'])
def main():
    data = request.json

    print(f"###############################\n{json.dumps(data)}\n#############################")  # Comment to hide what Telegram is sending you

    messages, chat_id = bot.reply(data)
    try:
        # Avoid flood
        if isinstance(messages, str):
            messages = [messages]
        elif messages == []:
            message = "No he podido sacar datos de ese producto"
            json_data = {
                "chat_id": chat_id,
                "text": message,
                'parse_mode': 'HTML'
            }
        else:
            for message in messages:
                json_data = {
                    "chat_id": chat_id,
                    "text": message,
                    'parse_mode': 'HTML'
                }

        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)
        return Response(json.dumps(json_data), status=200, mimetype='application/json')
    except Exception as e:
        print(f"<<--------------- Exception happens ---------\n{e}\n-----------End--------->>")
        json_data = {
            "chat_id": chat_id,
            "text": "Ha habido un error inesperado con ese producto",
            'parse_mode': 'HTML'
        }
        requests.post(message_url, json=json_data)  # This can avoid memory leaks
        return Response(json.dumps({"Error": e}), status=500, mimetype='application/json')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    env = os.environ.get('ENV', 'DEV')
    if env == 'PRD':
        debug = False
    else:
        debug = True
    xbot_webservice.run(host='0.0.0.0', port=port, debug=debug)
