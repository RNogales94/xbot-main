from utils.singleton import Singleton


@Singleton
class Bot:
    def __init__(self):
        self.__handle_intent = {
            'salutation': self.__start
        }

    def reply(self, message):
        intent = self.__get_intent(message)
        self.__handle_intent[intent](message)

    def __get_intent(self, message):
        return 'salutation'

    def __start(self, message):
        return 'Hola! Bienvenido a Xbot'
