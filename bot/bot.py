from utils.singleton import Singleton
from random import choice
from utils.url_utils import contain_urls, capture_urls
from scraper_proxy.proxy import Proxy
from xbot.utils.product import ProductFactory
from bot.message import Message


@Singleton
class Bot:
    def __init__(self):
        self.__handle_intent = {
            'salutation': self.__welcome,
            'no_intent': self.__not_understood,
            'url_detected': self.__show_urls,
            'format_urls': self.__format_urls,
        }

    def reply(self, message, chat_id):
        """

        :param message:
        :param chat_id:
        :return:
        """
        intent = self.__get_intent(message)
        message = self.__reply_to(intent, message)

        return message, chat_id

    def __reply_to(self, intent, message):
        message_handler = self.__handle_intent[intent]
        response_text = message_handler(message)

        return response_text

    @staticmethod
    def __get_intent(message):
        if message == "/start":
            return 'salutation'
        if contain_urls(message):
            return 'format_urls'
        return 'no_intent'

    @staticmethod
    def __not_understood(message):
        responses = ['No he entendido que quieres decir con eso',
                      'No lo he entendido, prueba con algo diferente',
                      'No he entendido eso, prueba con una URL o un comando',
                      'Lo siento, no se que decir a eso'
        ]

        return [choice(responses)]

    @staticmethod
    def __welcome(message):
        return ['Hola! Bienvenido a Xbot']

    @staticmethod
    def __show_urls(message):
        urls = capture_urls(message)
        return urls

    @staticmethod
    def __format_urls(message):
        print("<<<<<<<<<<<<<<<<<<<<<<< Format url trace ")
        urls = capture_urls(message)
        print(urls)
        responses = Proxy().scrape(urls)
        print("Scrape response")
        print(responses)
        products = [ProductFactory.build_product_from_json(obj) for obj in responses]
        print("Products built")
        print(products)
        messages = [Message(product) for product in products]
        print("Messages")
        print(messages)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return messages




