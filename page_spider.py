import guardian
import habr
import json
from datetime import date
import pyrebase

config = {
    "apiKey": "AIzaSyB4S5tsqKCZnGbCTEkm8wCRKGimafQfprY",
    "authDomain": "quick-reader-2bca7.firebaseapp.com",
    "databaseURL": "https://quick-reader-2bca7.firebaseio.com",
    "projectId": "quick-reader-2bca7",
    "storageBucket": "quick-reader-2bca7.appspot.com",
    "messagingSenderId": "190636552524",
    "appId": "1:190636552524:web:d097c7dea575375b1b5fe9"}


def main():

    path_on_cloud = "news.txt"
    local_path = "news.txt"
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()

    storage.child(path_on_cloud).download(path_on_cloud)

    today = date.today()

    x = habr.grab_page()
    y = guardian.grab_page()
    z = x.append(y, ignore_index=True)

    list_of_articles = []
    for i in range(0, len(z)):
        title = z.iloc[i]['Article Title']
        author = z.iloc[i]['Author']
        body = z.iloc[i]['Article']
        thumb = z.iloc[i]['Img_url']
        photo = z.iloc[i]['Img_url']
        aspect_ratio = 1.5
        published_date = today.strftime("%B %d, %Y")
        article_obj = {"id": str(i + 1), "title": title, "author": author, "body": body, "thumb": thumb, "photo": photo,
                       "aspect_ratio": aspect_ratio, "published_date": published_date}
        list_of_articles.append(article_obj)

    final_s = json.dumps(list_of_articles)

    with open("news.txt", "w") as text_file:
        print(final_s, file=text_file)

    storage.child(path_on_cloud).put(local_path)


if __name__ == "__main__":
    main()
