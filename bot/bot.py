from utils.singleton import Singleton


@Singleton
class Bot:
    def __init__(self):
        self.__handle_intent = {
            'salutation': self.__start
        }

    def reply(self, message, chat_id):
        """

        :param message:
        :param chat_id:
        :return:
        """
        intent = self.__get_intent(message)
        self.__handle_intent[intent](message)

        return message, chat_id

    def __get_intent(self, message):
        print(f"Received message: {message}")
        return 'salutation'

    def __start(self, message):
        return 'Hola! Bienvenido a Xbot'
