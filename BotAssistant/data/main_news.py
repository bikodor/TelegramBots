import requests
from bs4 import BeautifulSoup

def get_main_news_ru():

    response = []
    try:
        URL = 'https://lenta.ru/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        item = soup.find('a', class_='card-mini _compact')
        title = item.find('h3')
        title_text = title.get_text(strip=True)
        link = 'https://lenta.ru/' + item['href']
        title_text = title_text.replace('\xa0', ' ')
        object_news = {'title': title_text, 'link': link}
        response.append(['Лента: ', object_news])

    except:
        pass

    try:
        URL = 'https://meduza.io/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        item = soup.find('a', class_='Link-module-root Link-module-isInBlockTitle')
        title = item.find('span')
        title_text = title.get_text(strip=True)
        link = 'https://meduza.io' + item['href']
        title_text = title_text.replace('\xa0', ' ')
        object_news = {'title': title_text, 'link': link}
        response.append(['Медуза: ', object_news])
    except:
        pass

    try:
        URL = 'https://ria.ru/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        item = soup.find('a', class_='cell-main-photo__link')
        title = soup.find('div', 'cell-main-photo__title')
        title_text = title.get_text(strip=True)
        link = item['href']
        title_text = title_text.replace('\xa0', ' ')
        object_news = {'title': title_text, 'link': link}
        response.append(['РИА Новости: ', object_news])
    except:
        pass

    try:
        URL = 'https://www.bbc.com/russian'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        item = soup.find_all('a', class_='focusIndicatorDisplayBlock bbc-uk8dsi e1d658bg0')
        item_last = item[1]
        title = item_last.find('span')
        link = item_last['href']
        title_text = title.get_text(strip=True)
        title_text = title_text.replace('\xa0', ' ')
        object_news = {'title': title_text, 'link': link}
        response.append(['BBC Russia: ', object_news])
    except:
        pass

    return response

def get_main_news_en():
    response = []
    try:
        URL = 'https://edition.cnn.com/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        item = soup.find('a', class_='container__title-url container_lead-package__title-url')
        title = item.find('h2', class_='container__title_url-text container_lead-package__title_url-text')
        title_text = title.get_text(strip=True)
        link = 'https://edition.cnn.com' + item['href']
        title_text = title_text.replace('\xa0', ' ')
        object_news = {'title': title_text, 'link': link}
        response.append(['CNN News: ', object_news])

    except:
        pass
    try:

        URL = 'https://www.nbcnews.com/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        item = soup.find('h2', class_='storyline__headline founders-cond fw6 lead headlineOnly')
        title = item.find('a')
        title_text = title.get_text(strip=True)
        link = title['href']
        title_text = title_text.replace('\xa0', ' ')
        object_news = {'title': title_text, 'link': link}
        response.append(['NBC News: ', object_news])

    except:
        pass
    try:
        URL = 'https://www.bbc.com/news/world/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        item = soup.find('a', class_='sc-4befc967-1 gzOvMy')
        title = soup.find('h2')
        title_text = title.get_text(strip=True)
        link = 'https://www.bbc.com/news/world/' + item['href']
        title_text = title_text.replace('\xa0', ' ')
        object_news = {'title': title_text, 'link': link}
        response.append(['World BBC News: ', object_news])
    except:
        pass
    try:
        URL = 'https://www.foxnews.com/'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        item = soup.find('h3', class_='title')
        item_a = item.find('a')
        link = item_a['href']
        title_text = item_a.get_text(strip=True)
        title_text = title_text.replace('\xa0', ' ')
        object_news = {'title': title_text, 'link': link}
        response.append(['Fox News: ', object_news])
    except:
        pass
    return response
