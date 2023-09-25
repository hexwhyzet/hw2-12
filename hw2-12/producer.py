import json
from functools import partial

import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from dal.post import Post
from dal.repository import get_sessionmaker, get_repository
from dal.user import User, user_following
from keyval import get_posts
from messages import message_broker

QUEUE = 'feed'

app = FastAPI(debug=True)

connection = message_broker()
channel = connection.channel()

channel.queue_declare(queue=QUEUE)

sessionmaker = get_sessionmaker()


def user_to_dict(user: User):
    return {
        "id": user.id,
        "name": user.name
    }


def post_to_dict(post: Post):
    return {
        "id": post.id,
        "text": post.text,
        "user_id": post.user_id
    }


depends = Depends(partial(get_repository, sessionmaker))


class CreateUserData(BaseModel):
    name: str


class CreatePostData(BaseModel):
    text: str


@app.post("/user/create")
def create_user(create_user_data: CreateUserData, repository=depends):
    user = User(name=create_user_data.name)
    repository.add(user)
    return user_to_dict(user)


@app.get("/user/{user_id}")
def get_user(user_id, repository=depends):
    user = repository.get_by_id(User, id=user_id)
    return user_to_dict(user)


@app.post("/user/{user_id}/create_post")
def create_post(user_id: int, create_post_data: CreatePostData, repository=depends):
    post = Post(text=create_post_data.text, user_id=user_id)
    repository.add(post)
    data = {
        "user_id": user_id,
        "post_id": post.id
    }
    channel.basic_publish(exchange='', routing_key=QUEUE, body=json.dumps(data))
    return post_to_dict(post)


@app.get("/post/{post_id}")
def get_post(post_id: int, repository=depends):
    post = repository.get_by_id(Post, id=post_id)
    return post_to_dict(post)


@app.get("/user/{user_id}/feed")
def get_feed(user_id: int):
    post_ids = get_posts(user_id, 5)
    return post_ids


@app.post("/user/{user_id}/subscribe/{leader_id}", status_code=200)
def post_subscribe(user_id: int, leader_id: int, repository=depends):
    user = repository.get_by_id(User, id=user_id)
    leader = repository.get_by_id(User, id=leader_id)
    user.following.append(leader)
    repository.update(user)
    return


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
