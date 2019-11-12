import json
from flask import Flask, request, Response
from flask_cors import CORS
from xbot.xbotdb import Xbotdb
from bot_handler.telegram_config import BOT_URL
from bot_handler.bot import Bot
import requests
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
            for chat_id, user in [(id, xbotdb.get_user_by_chat_id(id)) for id in [213337828, 9623929, 24843237]]:
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
            message = messages
            json_data = {
                "chat_id": chat_id,
                "text": message,
                'parse_mode': 'HTML'
            }
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
