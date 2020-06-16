import json
from copy import deepcopy
from random import randint, sample

import requests

from faker import Faker

from config_reader import NUMBER_OF_USERS, DEFAULT_PASSWORD, SERVER_URL, MAX_POSTS_PER_USERS, MAX_LIKES_PER_USERS

fake = Faker()


class ClientError(Exception):
    pass


def authorized_request(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in args[0].base_request.headers.keys():
            raise ClientError('Can not perform request without authorization headers')
        func(*args, **kwargs)

    return wrapper


class BotUser:

    def __init__(self, server_url: str, username: str, password: str):
        self.api_url = '/'.join(('http:/', server_url, 'api'))
        self.base_request = requests.Request(url=self.api_url)
        self.username = username
        self.password = password
        self.created_posts_ids = set()
        self.session = requests.Session()

    def register(self):
        request = deepcopy(self.base_request)
        request.method = 'POST'
        request.url += '/user/register/'
        request.data = {
            'username': self.username,
            'password': self.password
        }

        response = self.session.send(request.prepare())
        if response.status_code != 201:
            raise ClientError(response.content)

    def login(self):
        if not self.username or not self.password:
            raise ClientError('Can not login without email or username')

        request = deepcopy(self.base_request)
        request.method = 'POST'
        request.url += '/user/login/'
        request.data = {
            'username': self.username,
            'password': self.password
        }

        response = self.session.send(request.prepare())
        if response.status_code != 200:
            raise ClientError(response.content)

        jwt = json.loads(response.content)['access']
        self.base_request.headers.update(
            {'Authorization': ' '.join(('Bearer', jwt))}
        )

    @authorized_request
    def create_post(self):
        post_title = fake.sentence(nb_words=3)
        post_text = fake.text()

        request = deepcopy(self.base_request)
        request.method = 'POST'
        request.url += '/post/'
        request.data = {
            'title': post_title,
            'content': post_text
        }

        response = self.session.send(request.prepare())

        if response.status_code != 201:
            raise ClientError(response.content)

        response_body = json.loads(response.content)
        self.created_posts_ids.add(response_body['id'])

    @authorized_request
    def like_post(self, post_id: int):
        request = deepcopy(self.base_request)
        request.method = 'POST'
        request.url += f'/post/{str(post_id)}/like/'

        response = self.session.send(request.prepare())

        if response.status_code != 201:
            raise ClientError(response.content)


def register_users(server_url: str, number_of_users: int, default_password: str) -> set:
    users = set()
    while len(users) < number_of_users:
        username = '_'.join((fake.first_name(), str(randint(0, int(number_of_users)))))
        user = BotUser(server_url=server_url, username=username, password=default_password)
        try:
            user.register()
        except ClientError as e:
            print(e)
            continue
        users.add(user)
    return users


def bots_master():
    posts_ids = set()
    users = register_users(number_of_users=int(NUMBER_OF_USERS),
                           default_password=DEFAULT_PASSWORD,
                           server_url=SERVER_URL)
    for user in users:
        try:
            user.login()
            for _ in range(int(MAX_POSTS_PER_USERS)):
                user.create_post()
            posts_ids.update(user.created_posts_ids)
        except ClientError as e:
            print(e)
            continue

    for user in users:
        post_to_like_ids = sample(posts_ids, int(MAX_LIKES_PER_USERS))
        for post_id in tuple(post_to_like_ids):
            try:
                user.like_post(post_id=post_id)
            except ClientError as e:
                print(e)
                continue


if __name__ == "__main__":
    bots_master()
