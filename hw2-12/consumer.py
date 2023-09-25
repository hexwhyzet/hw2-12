import json
import os
import sys

from dal.repository import get_sessionmaker, SQLAlchemyRepository
from dal.user import User
from keyval import add_post
from messages import message_broker

QUEUE = 'feed'

sessionmaker = get_sessionmaker()


def callback(ch, method, properties, body):
    session = sessionmaker()
    repository = SQLAlchemyRepository(session)
    data = json.loads(body)
    user_id = data['user_id']
    post_id = data['post_id']
    print(user_id, post_id)
    user = repository.get_by_id(User, id=user_id)
    for follower in user.followers:
        add_post(follower.id, post_id)
    session.close()


def main():
    connection = message_broker()
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE)

    channel.basic_consume(queue=QUEUE, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
