from content_scaper import scrape_new_posts, preproccess_url
from summarise import summarize_text
from formatter import make_body
from lemmy_poster import post
import time


import json
from newspaper import Article
from db import add_seen_item

import os


# Function to be called when a new RSS item is detected
def on_new_item(feed, entry):
    
    url = entry.link
    title = entry.title
    print("Working on new article: {}, {}".format(url, title))

    article = Article(preproccess_url(url)) # only proxy the url for requesting purposes
    article.download()
    article.parse()

    author = entry.author
    published = article.publish_date
    text = article.text
    images = json.dumps(article.images)
    title_images = json.dumps([x["url"] for x in entry.media_content if x["medium"]=="image"])
    print("Scraped")

    summary = summarize_text(text)
    print("Summarised")

    if not os.environ["POST_REVIEW"]:
        body = make_body(text, summary, author, published)
        post(title, url, body)
        print("Posted")

    add_seen_item(feed, url, title, author, published, text, summary, images, title_images, not os.environ["POST_REVIEW"])
    print("Added to db")


def main():
    while True:
        scrape_new_posts(on_new_item)
        time.sleep(10)

if __name__ == "__main__":
    main()