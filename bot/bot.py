from utils.singleton import Singleton
from random import choice
from utils.url_utils import contain_urls, capture_urls
from scraper_proxy.proxy import Proxy
from xbot.utils.product_factory import ProductFactory
from bot.message_customizer import MessageCustomizer
from xbot.xbotdb import Xbotdb
from xbot.models.user import User
from bot.message import Message
from utils.register_utils import is_register_message

db = Xbotdb()


@Singleton
class Bot:
    def __init__(self):
        self.__handle_intent = {
            'salutation': self.__welcome,
            'no_intent': self.__not_understood,
            'url_detected': self.__show_urls,
            'format_urls': self.__format_urls,
            'register': self.__register
        }

    def reply(self, message, chat):
        """
        reply to the indicate user an appropiate response based on the incoming message.
        Internally it detect the intent and create a custom response for the user caller.

        :param message:
        :param chat: dictionary with id, username and is_bot
        :return: message, chat_id
        """
        chat_id = chat['id']
        intent = self.__get_intent(message)
        message = self.__reply_to(intent, message, chat)

        return message, chat_id

    def __reply_to(self, intent, message, chat):

        message_handler = self.__handle_intent[intent]
        response_text = message_handler(message, chat)

        return response_text

    @staticmethod
    def __create_new_user(chat):
        new_user = User(chatId=chat['id'], telegramName=chat['username'])
        db.insert_user(user=new_user)

    @staticmethod
    def __get_intent(message):
        if is_register_message(message):
            return 'register'
        if message == "/start":
            return 'salutation'
        if contain_urls(message):
            return 'format_urls'
        return 'no_intent'

    @staticmethod
    def __not_understood(message, chat=None):
        responses = ['No he entendido que quieres decir con eso',
                      'No lo he entendido, prueba con algo diferente',
                      'No he entendido eso, prueba con una URL o un comando',
                      'Lo siento, no se que decir a eso'
        ]

        return [choice(responses)]

    def __welcome(self, message, chat):
        # if user is not registered register user
        user = db.get_user_by_chat_id(chat['id'])
        if user is None:
            self.__create_new_user(chat)
        return [f'Hola ! Bienvenido a Xbot usa /help para ver las opciones de configuración']

    @staticmethod
    def __register(message):
        """
        Create a new user from a message such as /register <amazon_tag>
        :param message:
        :return: Message of success or fail
        """




    @staticmethod
    def __show_urls(message, chat=None):
        urls = capture_urls(message)
        return urls

    @staticmethod
    def __format_urls(message, chat):
        print("<<<<<<<<<<<<<<<<<<<<<<< Format url trace ")
        urls = capture_urls(message)
        user = db.get_user_by_chat_id(chat_id=chat['id'])
        print(urls)
        responses = Proxy().scrape(urls)
        print("Scrape response")
        print(responses)
        products = [ProductFactory.build_product_from_json(obj['data']) for obj in responses]
        print("Products built")
        print(products)
        messages = [MessageCustomizer.build_message(product, user) for product in products]
        print("Messages")
        print(messages)
        text_messages = [str(message) for message in messages]
        print("text messages")
        print(text_messages)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return text_messages




