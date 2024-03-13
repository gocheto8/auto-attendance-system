import datetime
import json
import logging
import os
import recognizer
import pika
from pika.exchange_type import ExchangeType

'''RabbitMQ settings'''
EXCHANGE = u'main'
EXCHANGE_TYPE = ExchangeType.direct
CONSUME_ROUTING_KEY = u'recognizer_queue'
RESULT_ROUTING_KEY = u'record_queue'
CONSUME_QUEUE = u'recognizer_queue'
RESULT_QUEUE = u'record_queue'
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, connection_attempts=3, credentials=credentials)


'''Recognizer settings'''
os.chdir('./recognizer_service_v1')
TREE_FILE = './resources/face_embeddings_index.ann'
METRIC = 'euclidean'
VECTOR_SIZE = 512
MAX_DIST = 17


'''logger settings'''
LOG_FORMAT = '%(levelname)-10s %(asctime)s %(name)s %(funcName)s %(lineno)-4d: %(message)s'
logging.basicConfig(filename='./consumer_app.log', level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)

rec = recognizer.Recognizer(TREE_FILE, VECTOR_SIZE, METRIC)

def recognize(channel, method_frame, header_frame, body) -> None:
    data = json.loads(body)
    index = rec.recognize(data['embedding'])
    dist: float = index[1][0]
    LOGGER.info(f"Recognized person with id {index[0][0]} and distance {index[1][0]}")
    if dist > MAX_DIST:
        return
    
    del data['embedding']
    data["person_id"] = f"{index[0][0]:05}"
    data["distance"] = dist
    dt_object = datetime.datetime.fromtimestamp(data['time'])
    data["time"] = dt_object.strftime('%Y-%m-%dT%H:%M:%SZ')
    body = json.dumps(data)
    channel.basic_publish(
        EXCHANGE, RESULT_ROUTING_KEY, body,
        pika.BasicProperties(content_type='application/json',
                            delivery_mode=pika.DeliveryMode.Transient)
    )
    pass


LOGGER.info("Recognizer service is starting...")
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.exchange_declare(exchange=EXCHANGE,
                        exchange_type=EXCHANGE_TYPE,
                        passive=False,
                        durable=True,
                        auto_delete=False)
channel.queue_declare(CONSUME_QUEUE)
channel.queue_bind(CONSUME_QUEUE, EXCHANGE, CONSUME_ROUTING_KEY)

channel.queue_declare(RESULT_QUEUE)
channel.queue_bind(RESULT_QUEUE, EXCHANGE, RESULT_ROUTING_KEY)

connection.sleep(5)
LOGGER.info("Connection established.")

channel.basic_consume(queue=CONSUME_QUEUE, on_message_callback=recognize, auto_ack=True)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    connection.close();
    LOGGER.info('Connection closed. Application closing.')
