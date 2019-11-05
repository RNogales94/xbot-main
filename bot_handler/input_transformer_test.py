from bot_handler.input_transformer import InputTransformer
import json

with open('/home/rafa/PycharmProjects/xbot-main/bot_handler/test_inputs/edited_message.json') as json_file:
    edited_message = json.load(json_file)

with open('/home/rafa/PycharmProjects/xbot-main/bot_handler/test_inputs/edited_message2.json') as json_file:
    edited_message2 = json.load(json_file)

with open('/home/rafa/PycharmProjects/xbot-main/bot_handler/test_inputs/standard_message.json') as json_file:
    standard_message = json.load(json_file)

it = InputTransformer()

m, c, l = it.capture_input_data(edited_message)


def test_standard_message_input():
    message = standard_message
    assert isinstance(message, dict)
    assert isinstance(message['message'], dict)
    assert isinstance(message['message']['chat']['id'], int)
    assert isinstance(message['message']['text'], str)
    assert isinstance(message['message']['text'], str)
    assert "message" in message.keys()

    # capture links test
    amazon_link = 'https://www.amazon.es/dp/B07N2TJDKN?tag=hhhh'
    assert isinstance(it.capture_links(message), list)
    assert it.capture_links(message) == [amazon_link]

    # capture message test
    assert isinstance(it.capture_message(message), str)
    assert "https://www.amazon.es/dp/B07N2TJDKN?tag=hhhh" == it.capture_message(message)

    # capture chat id
    assert isinstance(it.capture_chat(message), dict)
    assert isinstance(it.capture_chat(message)['id'], int)
    assert it.capture_chat(message)['id'] == 213337828

    # global test
    data = it.capture_input_data(message)
    assert "https://www.amazon.es/dp/B07N2TJDKN?tag=hhhh" in data["message"]
    assert [amazon_link] == data["links"]
    assert 213337828 == data['chat']['id']


def test_edited_message_input():
    assert isinstance(edited_message, dict)
    assert isinstance(edited_message['edited_message'], dict)
    assert isinstance(edited_message['edited_message']['chat']['id'], int)
    assert isinstance(edited_message['edited_message']['text'], str)
    assert isinstance(edited_message['edited_message']['text'], str)
    assert "edited_message" in edited_message.keys()

    # capture links test
    amazon_link = 'https://www.amazon.es/dp/B07YTHJW5X?tag=koko01a-21'
    assert isinstance(it.capture_links(edited_message), list)
    assert it.capture_links(edited_message) == [amazon_link]

    # capture message test
    assert isinstance(it.capture_message(edited_message), str)
    assert "kisshes Hombres Chaquetas" in it.capture_message(edited_message)

    # capture chat id
    assert isinstance(it.capture_chat(edited_message), dict)
    assert isinstance(it.capture_chat(edited_message)['id'], int)
    assert it.capture_chat(edited_message)['id'] == 9623929

    # global test
    data = it.capture_input_data(edited_message)
    assert "kisshes Hombres Chaquetas" in data["message"]
    assert [amazon_link] == data["links"]
    assert 9623929 == data['chat']['id']

    # Edited message 2
    edited_message2
    assert isinstance(edited_message2, dict)
    assert isinstance(edited_message2['edited_message'], dict)
    assert isinstance(edited_message2['edited_message']['chat']['id'], int)
    assert isinstance(edited_message2['edited_message']['text'], str)
    assert isinstance(edited_message2['edited_message']['text'], str)
    assert "edited_message" in edited_message2.keys()

    # capture links test
    amazon_link = 'https://www.amazon.es/dp/B07ZJC8SS6?tag=koko01a-21'
    assert isinstance(it.capture_links(edited_message2), list)
    assert it.capture_links(edited_message2) == [amazon_link]

    # capture message test
    assert isinstance(it.capture_message(edited_message2), str)
    assert "kisshes Toy Mini Cars" in it.capture_message(edited_message2)

    # capture chat id
    assert isinstance(it.capture_chat(edited_message2), dict)
    assert isinstance(it.capture_chat(edited_message2)['id'], int)
    assert it.capture_chat(edited_message2)['id'] == 9623929

    # global test
    data = it.capture_input_data(edited_message2)
    assert "kisshes Toy Mini Cars " in data["message"]
    assert [amazon_link] == data["links"]
    assert 9623929 == data['chat']['id']



