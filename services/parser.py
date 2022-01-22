from bs4 import BeautifulSoup
import requests

from services.db import save_news


class Parser:
    url = None
    football_news_url = None

    def __init__(self):
        self.url = "https://www.sports.ru"
        self.football_news_url = "/football/news/"

    def parse_all_news(self):
        page = 1
        while requests.get(self.url + self.football_news_url + '/?page=' + str(page)) and page <= 20:
            site_response = requests.get(self.url + self.football_news_url + '/?page=' + str(page))
            news_soup = BeautifulSoup(site_response.text, 'lxml')
            news_list = news_soup.findAll('div', class_='short-news')
            page += 1
            for news in news_list:
                news_link = news.find('a', class_='short-text').get('href')
                self.parse_news(news_link)


    def parse_news(self, url):
        news_response = requests.get(self.url + url)
        news_soup = BeautifulSoup(news_response.text, 'lxml')
        news_header = news_soup.find(class_='news-item__header')
        news_date = news_header.find(class_='news-item__social-line').find(class_='time-block').get('datetime')
        news_title = news_header.h1.text.strip()

        text = ''
        news_content = news_soup.find(class_='news-item__content').findAll('p')
        for i in news_content:
            text += i.text + '\n'

        news_info = {
            'date': news_date,
            'title': news_title,
            'text': text
        }

        save_news(news_info)
