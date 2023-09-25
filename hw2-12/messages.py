import os

from pika import ConnectionParameters, BlockingConnection, PlainCredentials, URLParameters

FEED_QUEUE = 'feed'


def message_broker():
    credentials = PlainCredentials('guest', 'guest')
    return BlockingConnection(
        URLParameters("amqp://guest:guest@rabbitmq/")
        # ConnectionParameters(
        #     host=os.getenv('RABBITMQ_HOST'),
        #     port=int(os.getenv('RABBITMQ_PORT')),
        #     virtual_host='/',
        #     credentials=credentials
        # )
    )
