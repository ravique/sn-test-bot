# Social Network Bot Demo

Simple bot, that fills [Social Network Demo](https://github.com/ravique/social-network-demo) with example content . Was made as a test task. [Technical specification](TASK.md)

## Install
```commandline
git clone https://github.com/ravique/sn-test-bot.git
cd sn-test-bot
pip install -r requirements.txt
```

then add `config.ini` to the `sn-test-bot` folder.

example:
```ini
[SERVER]
url = localhost:8000

[BOT]
number_of_users = 2
max_posts_per_user = 2
max_likes_per_user = 2
default_password = notcommonpassword1024
```

Default parameters:
```
'url': 'localhost',
'number_of_users': 10,
'max_posts_per_user': 10,
'max_likes_per_user': 10,
'default_password': 'notcommonpassword1024'
```

## Authors

* **Andrei Etmanov**

## License

This project is licensed under the MIT License – see the [LICENSE.md](LICENSE.md) file for details