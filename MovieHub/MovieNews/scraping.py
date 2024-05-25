from datetime import timedelta, datetime
import requests
from bs4 import BeautifulSoup


# avrà il compito di prendere ogni singolo canale e di tirare fuori le news da esso
def update_news(rss_list):

    # for dei canali
    for channel in rss_list:
        last_update = channel.news[0].date
        current_time = datetime.now()
        difference = current_time - last_update
        hour = timedelta(hours=1)
        # se per quel canale, l'ultima notizia in DB ha meno di un ora allora per quel canale si hanno già le news aggiornate
        if difference >= hour:
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
        news.object.create(
            news_title = a.find('title').text,
            description = descr,
            short_description = ' '.join(short_split),
            imagine = a.find('enclosure').get('url'),
            date = date,
            rss_model = channel
        )
