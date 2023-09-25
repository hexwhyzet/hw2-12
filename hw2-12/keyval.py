import os

import redis


def kvdb():
    return redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT')),
        # username="default",
        decode_responses=True,
        password=os.getenv('REDIS_PASSWORD')
    )


def get_feed_key(user_id: int):
    return f'feed_{user_id}'


def add_post(user_id: int, post_id: int):
    with kvdb() as db:
        db.lpush(get_feed_key(user_id), post_id)


def get_posts(user_id, n: int):
    with kvdb() as db:
        return db.rpop(get_feed_key(user_id), n)
