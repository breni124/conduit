import calendar
import time

user_data = {
    'username': 'tesztelo0124',
    'email': 'tesztelo0124@gmail.com',
    'password': 'Tesztelek2023',
}

article = {
    "title": "My first article" + str(calendar.timegm(time.gmtime())),
    "about": "My first lorem ipsum article",
    "article": "This is my first lorem ipsum article.",
    "tags": "lorem" "ipsum"
        }

modified_article = {
    "title": "My modified first article" + str(calendar.timegm(time.gmtime())),
    "about": "Test for my modified first article",
    "article": "This is my modified first lorem ipsum article",
    "tags": "lorem" "ipsum"
}