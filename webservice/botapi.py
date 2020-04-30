import os
import json
import requests
from datetime import datetime
from flask import Flask, request, Response
from flask_cors import CORS

from rabbit import Rabbit
from xbot.xbotdb import Xbotdb
from bot_handler.telegram_config import BOT_URL
from bot_handler.bot import Bot

from utils.regex_utils import get_coupon_info

xbot_webservice = Flask(__name__)
CORS(xbot_webservice)

xbotdb = Xbotdb()

bot = Bot()


@xbot_webservice.route("/")
def index():
    return 'xbot_proxy'


@xbot_webservice.route('/bot', methods=['POST'])
def get_user_feed():
    try:
        data = request.json
        chat_id, links, text = bot.get_feed(data)
        coupon = get_coupon_info(text)

        if text == '/start':
            user_response = 'Bienvenido a XBot, contacta con @RNogales para activar tu cuenta demo gratuitamente\nUsa /help para aprender como usar XBot'

        elif text == '/help':
            user_response = '/info Para otener información sobre Xbot\n/cupon CODIGO PRECIO URL\n/infocupon para informacion sobre /cupon'

        elif text == '/info':
            user_response = 'Xbot es una pareja de bots, @tg_xbot y @delivery_xbot. \nPuedes enviar links de Amazon o reenviar mensajes desde otros canales a @tg_xbot y @delivery_xbot te responderá.\nPero para activar tu cuenta necesitas enviar tu tag de amazon a @RNogales y añadir @delivery_xbot como administrador a un canal en el que quieras recibir las ofertas.\nXbot tambien puede buscar y enviarte ofertas automáticamente sin que tu hagas nada, incluso filtrar por categorias y extraer estadísticas de clicks de tus canales.'

        elif text == '/infocupon':
            user_response = 'Los centimos del precio deben separarse con punto (no vale coma) y el simbolo del € debe ir seguido sin espacios, tambien se puede usar el del $.\n\nSi el bot dice "cupon capturado" es que lo has hecho bien!'

        elif coupon is not None:
            code = coupon.get('code', None)
            final_price = coupon.get('final_price', None)
            links = coupon.get('urls', None)

            if (code is not None) and (final_price is not None) and (links is not None):
                for url in links:
                    message = {'origin': chat_id, 'url': url, 'coupon_code': code, 'coupon_price': final_price, 'time': datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}
                    Rabbit().log(body=message, routing_key='ManualFeed')
                user_response = f'Cupon Capturado:\nCODE: {code}\nPrecio: {final_price}\n {links[0]}'
        else:
            for url in links:
                message = {'origin': chat_id, 'url': url, 'time': datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}
                Rabbit().log(body=message, routing_key='ManualFeed')

            if len(links) == 0:
                user_response = 'No se ha capturado ningún link válido de Amazon, pruebe con otro mensaje'
            elif len(links) == 1:
                user_response = f'Link Capturado: {links[0]}'
            else:
                user_response = f'Links Capturados:\n{links}'

        json_data = {
            "chat_id": chat_id,
            "text": user_response,
            'parse_mode': 'HTML'
        }

        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)

        # Notify admin

        json_data[
            'text'] = f"To: {xbotdb.get_user_by_chat_id(json_data['chat_id']).telegram_name}\n{user_response}\nInput: {json.dumps(data)}"
        json_data['chat_id'] = 213337828

        requests.post(message_url, json=json_data)
    except Exception as e:
        try:
            # Notify error to admin

            json_data = {
                "chat_id": 213337828,
                "text": f"ERROR: {str(e)}",
                'parse_mode': 'HTML'
            }

            message_url = BOT_URL + 'sendMessage'
            requests.post(message_url, json=json_data)

            # Notify error to user
            data = request.json
            chat_id = data['chat']['id']

            json_data['chat_id'] = chat_id
            requests.post(message_url, json=json_data)

            return Response(json.dumps({'Error': str(e)}), status=200, mimetype='application/json')
        except Exception as e:
            print(f'VERY IMPORTANT ERROR: {e}\nreturning 200 to avoid infinite loop')
            return Response(json.dumps({'Error': str(e)}), status=200, mimetype='application/json')

    return Response(json.dumps(json_data), status=200, mimetype='application/json')

########################
#  OTHER API METHODS   #
########################
########################


@xbot_webservice.route('/api/v1/offers', methods=['GET'])
def get_offers():
    page = int(request.args.get('page', 0))
    max_items = int(request.args.get('max_items', 20))
    user_id = request.args.get('user_id')

    errors = []
    # Validations
    if page < 0 or max_items < 1:
        errors.append('page < 0 or max_items < 1')
        response = json.dumps({"products": [], "errors": errors})
        status = 404

    else:
        db = Xbotdb()
        offset = page * max_items
        products = db.get_products(skip=offset, limit=max_items, new_first=True)
        response = json.dumps({"products": products, "errors": []})
        status = 200

    return Response(response, mimetype='application/json', status=status)


@xbot_webservice.route('/api/v1/search', methods=['GET'])
def search_offers():
    text = request.args.get('text')
    min_discount = int(request.args.get('min_discount', 0))
    user_id = request.args.get('user_id')

    products = []
    response = json.dumps({"products": products, "errors": []})
    status = 200

    return Response(response, mimetype='application/json', status=status)


@xbot_webservice.route('/api/v1/set_alert', methods=['POST'])
def set_alert():
    data = request.json
    min_discount = int(data.get('min_discount', 0))
    text = data.get('text')
    user_id = data.get('user_id')

    response = {"min_discount": min_discount,
                "text": text,
                "user_id": user_id,
                "errors": []
                }
    status = 200

    return Response(response, mimetype='application/json', status=status)


@xbot_webservice.route('/api/v1/report_offer', methods=['POST'])
def report_offer():
    data = request.json
    offer_id = data.get('offer_id')
    user_id = data.get('user_id')

    response = {"offer_id": offer_id,
                "user_id": user_id,
                "errors": []
                }
    status = 200

    return Response(response, mimetype='application/json', status=status)


@xbot_webservice.route('/api/v1/rate_offer', methods=['POST'])
def rate_offer():
    data = request.json
    offer_id = data.get('offer_id')
    rate = data.get('rate')
    user_id = data.get('user_id')

    response = {"offer_id": offer_id,
                "rate": rate,
                "user_id": user_id,
                "errors": []
                }
    status = 200

    return Response(response, mimetype='application/json', status=status)


@xbot_webservice.route('/api/v1/offer_click', methods=['POST'])
def offer_click():
    data = request.json
    offer_id = data.get('offer_id')
    user_id = data.get('user_id')
    rate = True  # Implicit ratting

    response = {"offer_id": offer_id,
                "rate": rate,
                "user_id": user_id,
                "errors": []
                }
    status = 200

    return Response(response, mimetype='application/json', status=status)


@xbot_webservice.route('/api/v1/get_news', methods=['GET'])
def get_news():
    user_id = request.args.get('user_id')

    products = []
    response = json.dumps({"products": products, "errors": []})
    status = 200

    return Response(response, mimetype='application/json', status=status)


@xbot_webservice.route('/api/v1/notification_click', methods=['POST'])
def notification_click():
    data = request.json
    offer_id = data.get('offer_id')
    user_id = data.get('user_id')
    timestamp_arrival = data.get('timestamp_arrival')

    rate = True  # Implicit ratting

    response = {"offer_id": offer_id,
                "rate": rate,
                "user_id": user_id,
                "timestamp_arrival": timestamp_arrival,
                "errors": []
                }
    status = 200

    return Response(response, mimetype='application/json', status=status)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    env = os.environ.get('ENV', 'DEV')
    if env == 'PRD':
        debug = False
    else:
        debug = True
    xbot_webservice.run(host='0.0.0.0', port=port, debug=debug)
