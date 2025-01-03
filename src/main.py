from content_scaper import scrape_new_posts, preproccess_url
from summarise import summarise_text
from formatter import make_body
from lemmy_poster import post
import time

import json
from newspaper import Article

from db import add_post

import os


# Function to be called when a new RSS item is detected
def on_new_item(feed, entry):
    url = entry.link
    title = entry.title
    print("Working on new article: {}, {}".format(url, title))

    proccessed_url, was_proccessed = preproccess_url(url)

    article = Article(proccessed_url) # only proxy the url for requesting purposes
    article.download()
    article.parse()


    try:
        author = entry.author
    except AttributeError:
        author = "Unknown"
    published = article.publish_date
    text = article.text
    images = json.dumps(article.images)
    try:
        title_images = json.dumps([x["url"] for x in entry.media_content if x["medium"]=="image"])
    except AttributeError:
        title_images = json.dumps(list())
    print("Scraped")

    scraped = True
    if text.strip() == "":
        scraped = False
        print("Could not scrape text skipping")

    summary = summarise_text(text)
    print("Summarised")

    if not os.environ["POST_REVIEW"]:
        body = make_body(text, summary, author, published)
        post(title, url, body)
        print("Posted")


    add_post(feed, url, title, author, published, text, summary, images, title_images, scraped, not os.environ["POST_REVIEW"])
    print("Added to db")

import click



@click.command()
@click.option('--retry', is_flag=True, help='retry posts with errors')
def main(retry):
    while True:
        # scrape new items without retrying failed scrapes
        scrape_new_posts(on_new_item, retry)
        time.sleep(10)

if __name__ == "__main__":
    main()