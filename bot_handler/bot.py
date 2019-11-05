from utils.singleton import Singleton
from random import choice
from utils.url_utils import contain_urls, capture_urls
from scraper_proxy.proxy import Proxy
from xbot.utils.product_factory import ProductFactory
from bot_handler.message_customizer import MessageCustomizer
from bot_handler.input_transformer import InputTransformer
from xbot.xbotdb import Xbotdb
from xbot.models.user import User
from utils.regex_utils import is_change_tag_message, get_amazon_tag, get_coupon_info

db = Xbotdb()
it = InputTransformer()


class Bot(metaclass=Singleton):
    def __init__(self):
        self.__handle_intent = {
            'start': self.__start,
            'help': self.__help,
            'no_intent': self.__not_understood,
            'build_product_message': self.__build_product_message,
            'tag': self.__tag
        }

    @staticmethod
    def __get_intent(data):
        message = data['message']
        links = data['links']

        if is_change_tag_message(message):
            return 'tag'
        if message == "/start":
            return 'start'
        if message == "/help":
            return 'help'
        if contain_urls(message) or len(links):
            return 'build_product_message'
        return 'no_intent'

    def reply(self, data_json):
        """
        reply to the indicate user an appropiate response based on the incoming message.
        Internally it detect the intent and create a custom response for the user caller.

        :param data_json: request body from telegram
        :return: message, chat
        """

        data = it.capture_input_data(data_json)
        chat_id = data['chat']['id']

        intent = self.__get_intent(data)
        message = self.__reply_to(intent, data)

        return message, chat_id

    def __reply_to(self, intent, data):

        message_handler = self.__handle_intent[intent]
        response_text = message_handler(data)

        return response_text

    @staticmethod
    def __create_new_user(data):
        chat = data['chat']
        new_user = User(chatId=chat['id'], telegramName=chat['username'])
        db.insert_user(user=new_user)

    @staticmethod
    def __not_understood(data):
        responses = ['No he entendido que quieres decir con eso',
                      'No lo he entendido, prueba con algo diferente',
                      'No he entendido eso, prueba con una URL o un comando',
                      'Lo siento, no se que decir a eso'
        ]

        return [choice(responses)]

    def __start(self, data):
        # if user is not registered register user
        chat = data['chat']
        user = db.get_user_by_chat_id(chat['id'])
        if user is None:
            self.__create_new_user(chat)
        return [f'Hola ! Bienvenido a Xbot usa /help para ver las opciones de configuración']

    @staticmethod
    def __help(data):
        print('help')
        # return [f'Envia links de productos de amazon para conseguir un mensaje con la oferta lista para reenviar a tu canal!\n'
        #         f'\nLista de comandos disponibles:\n\n '
        #         f'/tag <new_tag>  --> Cambia tu tag de amazon\n'
        #         f'/cupon <CODE> <PRICE> <LINK> --> Crea un mensaje con cupon (importante no dejar espacios entre el precio y el simbolo del €)'
        #         f'/help --> Ver este mensaje de ayuda']
        return [f'/tag <new_tag> --  Cambia tu tag de amazon']

    @staticmethod
    def __tag(data):
        """
        Change tag from a message such as /tag <amazon_tag>
        :param message:
        :return: Message of success or fail
        """

        message = data['message']
        chat = data['chat']

        new_tag = get_amazon_tag(message)
        if new_tag is None:
            return ["Debes escribir una tag valida, solo puedes usar letras, numeros y -\nEjemplo: /tag mitag-01"]
        try:
            user = db.get_user_by_chat_id(chat_id=chat['id'])

            db.update_user_tag(user.get_telegram_name(), new_amazon_tag=new_tag)
            return [f"Perfecto tu tag ahora es {new_tag}"]
        except:
            return [f"Ha habido un error no esperado en /tag, por favor contacta con el administrador"]

    # @staticmethod
    # def __coupon_product(message, chat):
    #     cupon = get_coupon_info(message)
    #     user = db.get_user_by_chat_id(chat_id=chat['id'])
    #
    #     responses = Proxy().scrape(cupon['link'])
    #     products = [ProductFactory.build_product_from_json(obj['data']) for obj in responses]
    #     messages = [MessageCustomizer.build_message(product, user, cupon) for product in products]
    #     text_messages = [str(message) for message in messages]
    #     return text_messages



    @staticmethod
    def __build_product_message(data):
        print("<<<<<<<<<<<<<<<<<<<<<<< Format url trace ")

        message = data['message']
        chat = data['chat']
        urls = data['links']
        user = db.get_user_by_chat_id(chat_id=chat['id'])

        cupon = get_coupon_info(message)
        if cupon is not None:
            urls = cupon['urls']
        print(urls)
        responses = Proxy().scrape(urls)
        print("Scrape response")
        print(responses)
        responses = filter(lambda x: 'Error' not in x['data'].keys(), responses)
        products = [ProductFactory.build_product_from_json(obj['data']) for obj in responses]
        print("Products built")
        print(products)
        messages = [MessageCustomizer.build_message(product, user, cupon) for product in products]
        print("Messages")
        print(messages)
        text_messages = [str(message) for message in messages]
        print("text messages")
        print(text_messages)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        return text_messages




