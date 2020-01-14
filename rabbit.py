import pika
from settings import RABBIT_USER, RABBIT_PASS, RABBIT_HOST
import json


class Rabbit():
    def __init__(self):
        self.credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
        self.parameters = pika.ConnectionParameters(RABBIT_HOST,
                                                    5672,
                                                    RABBIT_USER,
                                                    self.credentials)

        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

        self.properties = pika.BasicProperties(
            app_id='manual-bot',
            content_type='application/json',
            content_encoding='utf-8',
            delivery_mode=2,
        )

    def log(self, body, routing_key='None'):
        self.channel.basic_publish(exchange='',
                                   routing_key=routing_key,
                                   properties=self.properties,
                                   body=json.dumps(body))
