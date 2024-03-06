# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import pika
from pika import DeliveryMode
from pika.exchange_type import ExchangeType
import json


'''RabbitMQ settings'''
EXCHANGE = 'main'
EXCHANGE_TYPE = ExchangeType.direct
ROUTING_KEY = u'recognizer_queue'
QUEUE = u'recognizer_queue'

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE,
                         exchange_type=EXCHANGE_TYPE,
                         passive=False,
                         durable=True,
                         auto_delete=False)
channel.queue_declare(QUEUE)
channel.queue_bind(QUEUE, EXCHANGE, ROUTING_KEY)

connection.sleep(5)

def send_message(data: dict):
    body = json.dumps(data)
    channel.basic_publish(
        EXCHANGE, ROUTING_KEY, body,
        pika.BasicProperties(content_type='application/json',
                            delivery_mode=DeliveryMode.Transient))

def close():
    connection.close()