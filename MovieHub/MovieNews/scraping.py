from datetime import timedelta, datetime

import pytz
import requests
from bs4 import BeautifulSoup
from .models import News

# avrà il compito di prendere ogni singolo canale e di tirare fuori le news da esso
def update_news(rss_list):
    scrape = False
    for channel in rss_list:
        first_news = channel.news.first()
        if first_news:
            last_update = first_news.date
            current_time = datetime.now(pytz.utc)
            difference = current_time - last_update
            hour = timedelta(hours=1)
            # se per quel canale, l'ultima notizia in DB ha meno di un ora allora
            # per quel canale si hanno già le news aggiornate
            if difference >= hour:
                scrape = True

        if not first_news or scrape:
            scraping(channel, channel.news.all())


def scraping(channel, news):
    # elimino le mews non aggiornate
    news.delete()

    # riaggiorno le news per quel canale
    page = requests.get(channel.url)
    soup = BeautifulSoup(page.content, features = 'xml')
    # si prendono solo i primi 5 item
    articles = soup.findAll('item', limit = 5)

    # aggiorno il DB
    for a in articles:
        descr = a.find('description').text
        short_split = descr.split()[:10]
        pubDate = a.find('pubDate').text
        date = datetime.strptime(pubDate, '%a, %d %b %Y %H:%M:%S %z')
        feed = News.objects.create(
            news_title = a.find('title').text,
            description = descr,
            short_description = ' '.join(short_split),
            imagine = a.find('enclosure').get('url'),
            date = date,
            rss_model = channel
        )
        feed.save()

if __name__ == '__main__':
    print("Esecuzione di un file errato")