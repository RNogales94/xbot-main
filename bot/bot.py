from utils.singleton import Singleton
from random import choice
from utils.url_utils import contain_urls, capture_urls


@Singleton
class Bot:
    def __init__(self):
        self.__handle_intent = {
            'salutation': self.__welcome,
            'no_intent': self.__not_understood,
            'url_detected': self.__show_urls
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

    @staticmethod
    def __get_intent(message):
        if message == "/start":
            return 'salutation'
        if contain_urls(message):
            return 'url_detected'
        return 'no_intent'

    def __(self, intent, message):
        message_handler = self.__handle_intent[intent]
        response_text = message_handler(message)

        return response_text


    @staticmethod
    def __not_understood(message):
        responses = ['No he entendido que quieres decir con eso',
                      'No lo he entendido, prueba con algo diferente',
                      'No he entendido eso, prueba con una URL o un comando',
                      'Lo siento, no se que decir a eso'
        ]

        return choice(responses)

    @staticmethod
    def __welcome(message):
        return 'Hola! Bienvenido a Xbot'


    @staticmethod
    def __show_urls(message):
        urls = capture_urls(message)
        return f"Detected {urls}"
