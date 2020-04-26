import requests
from bs4 import BeautifulSoup
import redis

class News38Scraper:
    def __init__(self):
        self.markup = requests.get('https://www.news38.de/braunschweig/').text
        self.r = redis.StrictRedis(host='localhost',charset="utf-8" ,port=6379, db=0, decode_responses=True)

    def parse(self):
        soup = BeautifulSoup(self.markup, 'html.parser')
        links = soup.findAll('a', {'class': 'teaser__link-image'})
        self.saved_links = []
        for link in links:
            href = link['href']
            headline = ''
            h2 = link.find('h2', {'class': 'headline'})
            if not h2 is None:
                headline = h2.get_text().strip()
                self.saved_links.append({'headline': headline, 'link': href})

    def store(self):
        for link in self.saved_links:
            self.r.set(link['headline'], link['link'])

    def send(self):
        links = [{'link': self.r.get(k), 'headline': k} for k in self.r.keys()]
        print(links)


def main():
    scraper = News38Scraper()
    scraper.parse()
    scraper.store()
    scraper.send()


if __name__ == '__main__':
    main()