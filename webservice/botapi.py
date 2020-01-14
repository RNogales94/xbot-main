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
        chat_id, links = bot.get_feed(data)

        for url in links:
            message = {'origin': chat_id, 'url': url, 'time': datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}
            Rabbit().log(body=message, routing_key='ManualFeed')

        if len(links) == 0:
            user_response = 'No se ha capturado ningún link válido de Amazon, pruebe con otro mensaje'
        if len(links) == 1:
            user_response = f'Link Capturado: {links[0]}'
        if len(links) > 1:
            user_response = f'Links Capturados:\n{links}'

        json_data = {
            "chat_id": chat_id,
            "text": user_response,
            'parse_mode': 'HTML'
        }

        message_url = BOT_URL + 'sendMessage'
        requests.post(message_url, json=json_data)

        # Notify admin

        json_data['text'] = f"To: {xbotdb.get_user_by_chat_id(json_data['chat_id']).telegram_name}\n{user_response}\nInput: {json.dumps(data)}"
        json_data['chat_id'] = 213337828

        requests.post(message_url, json=json_data)
    except Exception as e:
        return Response(json.dumps({'Error': str(e)}), status=200, mimetype='application/json')

    return Response(json.dumps(json_data), status=200, mimetype='application/json')


# @xbot_webservice.route('/bot', methods=['POST'])
# def main():
#     data = request.json
#     try:
#         messages, chat_id = bot.reply(data)
#         message_url = BOT_URL + 'sendMessage'
#
#         # Avoid flood
#         if isinstance(messages, str):
#             message = messages
#             json_data = {
#                 "chat_id": chat_id,
#                 "text": message,
#                 'parse_mode': 'HTML'
#             }
#
#             requests.post(message_url, json=json_data)
#
#         elif not messages:
#             message = "No he podido sacar datos de ese producto"
#             json_data = {
#                 "chat_id": chat_id,
#                 "text": message,
#                 'parse_mode': 'HTML'
#             }
#             requests.post(message_url, json=json_data)
#
#         else:
#             for message in messages:
#                 json_data = {
#                     "chat_id": chat_id,
#                     "text": message,
#                     'parse_mode': 'HTML'
#                 }
#                 requests.post(message_url, json=json_data)
#
#         # Notify admin
#         try:
#             json_data['text'] = f"To: {xbotdb.get_user_by_chat_id(json_data['chat_id']).telegram_name}\n{messages}\nInput: {json.dumps(data)}"
#             json_data['chat_id'] = 213337828
#
#             requests.post(message_url, json=json_data)
#         except Exception as e:
#             print(e)
#
#         return Response(json.dumps(json_data), status=200, mimetype='application/json')
#     except Exception as e:
#         print(f"<<--------------- Exception happens ---------\n{e}\n-----------End--------->>")
#         json_data = {
#             "chat_id": 213337828,
#             "text": "Ha habido un error inesperado",
#             'parse_mode': 'HTML'
#         }
#
#         message_url = BOT_URL + 'sendMessage'
#         requests.post(message_url, json=json_data)  # This can avoid memory leaks
#         return Response(json.dumps(json_data), status=200, mimetype='application/json')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    env = os.environ.get('ENV', 'DEV')
    if env == 'PRD':
        debug = False
    else:
        debug = True
    xbot_webservice.run(host='0.0.0.0', port=port, debug=debug)
