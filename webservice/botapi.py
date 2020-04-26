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
            user_response = 'Xbot es una pareja de bots, @tg_xbot y @delivery_xbot. \nPuedes enviar links de Amazon o reenviar mensajes desde otros canales a @tg_xbot y @delivery_xbot te responderá.\nPero para activar tu cuenta necesitas enviar tu tag de amazon a @RNogales y añadir @delivery_xbot como administrador a un canal en el que quieras recibir las ofertas.\nXbot tambien puede buscar y enviarte ofertas automáticamente sin que tu hagas nada, incluso filtrar por categorias y extraer estadísticas de clicks de tus canales.'

        elif coupon is not None:
            code = coupon.get('code', None)
            final_price = coupon.get('final_price', None)
            links = coupon.get('urls', None)

            if (code is not None) and (final_price is not None) and (links is not None):
                for url in links:
                    message = {'origin': chat_id, 'url': url, 'code': code, 'price': final_price, 'time': datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}
                    Rabbit().log(body=message, routing_key='ManualFeed')
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    env = os.environ.get('ENV', 'DEV')
    if env == 'PRD':
        debug = False
    else:
        debug = True
    xbot_webservice.run(host='0.0.0.0', port=port, debug=debug)
