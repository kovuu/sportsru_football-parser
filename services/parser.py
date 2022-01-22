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
        while requests.get(self.url + self.football_news_url + '/?page=' + str(page)) and page <= 1:
            print(self.url + self.football_news_url + '/?page=' + str(page))
            site_response = requests.get(self.url + self.football_news_url + '/?page=' + str(page))
            news_soup = BeautifulSoup(site_response.text, 'lxml')
            news_list = news_soup.findAll('div', class_='short-news')
            print(len(news_list))
            for news in news_list:
                news_links = news.findAll('a', class_='short-text')
                for link in news_links:
                    self.parse_news(link.get('href'))

            page += 1

    def parse_news(self, url):
        news_response = requests.get(self.url + url)
        print(self.url + url)
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

        print(news_info)

        save_news(news_info)
