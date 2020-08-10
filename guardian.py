from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import numpy as np


def grab_page():
    # url definition
    url = "https://www.theguardian.com/uk"
    user = 'yabraze@gmail.com'
    pwd = '12345qwerty'

    r1 = requests.get(url, auth=HTTPBasicAuth(user, pwd))
    # print(r1.status_code)

    # We'll save in coverpage the cover page content
    coverpage = r1.content

    soup1 = BeautifulSoup(coverpage, 'html5lib')
    coverpage_news = soup1.find_all('h3', class_='fc-item__title')
    # print(coverpage_news)
    # print(len(coverpage_news))

    number_of_articles = 5
    news_contents = []
    list_links = []
    list_titles = []
    list_img_url = []

    # for n in np.arange(0, len(coverpage_news)):
    for n in np.arange(0, number_of_articles):
        if "live" in coverpage_news[n].find('a')['href']:
            continue
        # Getting the link of the article
        link = coverpage_news[n].find('a')['href']
        list_links.append(link)

        # Getting the title
        title = coverpage_news[n].find('a').get_text()
        list_titles.append(title)

        # getting the article images
        list_img_url.append("https://www.verandamarine.com/wp-content/uploads/2018/05/Ocean-Background-300x300.jpg")

    for link in list_links:
        article = requests.get(link)
        article_content = article.content
        noodle_soup = BeautifulSoup(article_content, 'html5lib')

        body = noodle_soup.find_all('p')
        list_paragraphs = []
        for p in np.arange(0, len(body)):
            paragraph = body[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)
        news_contents.append(final_article)

    df_news = pd.DataFrame(
        {'Article Title': list_titles,
        'Article': news_contents,
        'Link': list_links,
        'Img_url': list_img_url,
         'Author': 'The Guardian'}
        )

    return df_news
