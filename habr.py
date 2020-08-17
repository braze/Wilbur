from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import time
import numpy as np


def grab_page():
    # url definition
    url = "https://habr.com/en/all/"

    r1 = requests.get(url)

    # We'll save in coverpage the cover page content
    coverpage = r1.content

    soup1 = BeautifulSoup(coverpage, 'html5lib')
    coverpage_news = soup1.find_all('a', class_="post__title_link")
    # print(coverpage_news)
    # print(len(coverpage_news))

    number_of_articles = 10
    news_contents = []
    list_links = []
    list_titles = []
    list_img_url = []

    for n in np.arange(0, number_of_articles):
        # Getting the link of the article
        link = coverpage_news[n].get('href')
        list_links.append(link)

        # Getting the title
        title = coverpage_news[n].get_text()
        list_titles.append(title)

    for link in list_links:
        article = requests.get(link)
        article_content = article.content
        noodle_soup = BeautifulSoup(article_content, 'html5lib')

        body = noodle_soup.find_all('div', class_="post__body post__body_full")
        list_paragraphs = []
        for p in np.arange(0, len(body)):
            img_url = body[p].find('img')
            if img_url is not None:
                img_url = img_url['src']
            else:
                img_url = "https://www.verandamarine.com/wp-content/uploads/2018/05/Ocean-Background-300x300.jpg"
            list_img_url.append(img_url)
            paragraph = body[p].get_text()
            list_paragraphs.append(paragraph)
            final_article = " ".join(list_paragraphs)
        news_contents.append(final_article)

    df_news = pd.DataFrame(
        {'Article Title': list_titles,
         'Article': news_contents,
         'Link': list_links,
         'Img_url': list_img_url,
         'Author': 'Habra'}
    )

    return df_news