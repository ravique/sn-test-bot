import configparser

config = configparser.ConfigParser({
    'url': 'localhost',
    'number_of_users': 10,
    'max_posts_per_user': 10,
    'max_likes_per_user': 10,
    'default_password': 'notcommonpassword1024'
})
config.read('config.ini')

SERVER_URL = config.get('SERVER', 'url')
NUMBER_OF_USERS = config.get('BOT', 'number_of_users')
MAX_POSTS_PER_USERS = config.get('BOT', 'max_posts_per_user')
MAX_LIKES_PER_USERS = config.get('BOT', 'max_likes_per_user')
DEFAULT_PASSWORD = config.get('BOT', 'default_password')