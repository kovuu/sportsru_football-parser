from peewee import *

db = PostgresqlDatabase(
    'sportsru',
    user='postgres',
    password='qwerty',
    host='0.0.0.0',
    port='5432'
)


class News(Model):
    date = DateField()
    title = CharField()
    text = TextField()

    class Meta:
        database = db


def save_news(news_info):
    print(news_info)
    if not News.get_or_none(title=news_info['title']):
        News.create(date=news_info['date'], title=news_info['title'], text=news_info['text'])


db.connect()
db.create_tables([News])
