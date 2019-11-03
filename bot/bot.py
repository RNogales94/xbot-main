from utils.singleton import Singleton
from random import choice
from utils.url_utils import contain_urls, capture_urls
from scraper_proxy.proxy import Proxy
from xbot.utils.product_factory import ProductFactory
from bot.message_customizer import MessageCustomizer
from xbot.xbotdb import Xbotdb
from xbot.models.user import User
from bot.message import Message
from utils.register_utils import is_change_tag_message, get_amazon_tag

db = Xbotdb()


@Singleton
class Bot:
    def __init__(self):
        self.__handle_intent = {
            'start': self.__start,
            'no_intent': self.__not_understood,
            'url_detected': self.__show_urls,
            'build_product_message': self.__build_product_message,
            'tag': self.__tag
        }

    @staticmethod
    def __get_intent(message):
        if is_change_tag_message(message):
            return 'tag'
        if message == "/start":
            return 'start'
        if contain_urls(message):
            return 'build_product_message'
        return 'no_intent'

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
    def __not_understood(message, chat=None):
        responses = ['No he entendido que quieres decir con eso',
                      'No lo he entendido, prueba con algo diferente',
                      'No he entendido eso, prueba con una URL o un comando',
                      'Lo siento, no se que decir a eso'
        ]

        return [choice(responses)]

    def __start(self, message, chat):
        # if user is not registered register user
        user = db.get_user_by_chat_id(chat['id'])
        if user is None:
            self.__create_new_user(chat)
        return [f'Hola ! Bienvenido a Xbot usa /help para ver las opciones de configuración']

    @staticmethod
    def __tag(message, chat):
        """
        Change tag from a message such as /tag <amazon_tag>
        :param message:
        :return: Message of success or fail
        """

        new_tag = get_amazon_tag(message)
        if new_tag is None:
            return ["Debes escribir una tag valida, solo puedes usar letras, numeros y -\nEjemplo: /tag mitag-01"]
        try:
            user = db.get_user_by_chat_id(chat_id=chat['id'])

            db.update_user_tag(user.get_telegram_name(), new_amazon_tag=new_tag)
            return [f"Perfecto tu tag ahora es {new_tag}"]
        except:
            return [f"Ha habido un error no esperado en /tag, por favor contacta con el administrador"]


    @staticmethod
    def __show_urls(message, chat=None):
        urls = capture_urls(message)
        return urls

    @staticmethod
    def __build_product_message(message, chat):
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




