from utils.singleton import Singleton
from utils.regex_utils import is_image_url, fix_url_if_comes_in_list, capture_urls


class InputTransformer(metaclass=Singleton):

    @staticmethod
    def __capture_links_from_entities(entities):
        entities = filter(lambda x: 'url' in x.keys(), entities)
        links = [e['url'] for e in entities]
        links = [fix_url_if_comes_in_list(url) for url in links]
        return links

    def __remove_image_links(self, links):
        links = filter(lambda x: not is_image_url(x), links)
        links = list(links)
        return links

    def capture_links(self, data_json):
        links = []
        msg_links = []
        entities_links = []

        if "edited_message" in data_json.keys():
            if 'text' in data_json['edited_message'].keys():
                text = data_json['edited_message']['text']
            else:
                text = data_json['edited_message']['caption']
            msg_links = capture_urls(text)

            entities = data_json["edited_message"].get("entities", None)
            if entities is not None:
                entities_links = self.__capture_links_from_entities(entities)
        if 'message' in data_json.keys():
            if 'text' in data_json['message'].keys():
                text = data_json['message']['text']
            else:
                text = data_json['message']['caption']

            msg_links = capture_urls(text)
            entities = data_json["message"].get("entities", None)
            if entities is not None:
                entities_links = self.__capture_links_from_entities(entities)

        links = list(set(msg_links + entities_links))
        links = self.__remove_image_links(links)

        return links

    @staticmethod
    def capture_message(data_json):
        message = None
        if "edited_message" in data_json.keys():
            try:
                message = data_json['edited_message']['text']
            except KeyError:
                message = data_json['edited_message']['caption']

        if 'message' in data_json.keys():
            try:
                message = data_json['message']['text']
            except KeyError:
                message = data_json['message']['caption']

        return message

    @staticmethod
    def capture_chat(data_json):
        chat = None
        if "edited_message" in data_json.keys():
            chat = data_json['edited_message']['chat']

        if 'message' in data_json.keys():
            chat = data_json['message']['chat']

        return chat

    def capture_input_data(self, data_json):
        links = self.capture_links(data_json)
        message = self.capture_message(data_json)
        chat = self.capture_chat(data_json)

        data = {"message": message, "chat": chat, "links": links}
        return data
