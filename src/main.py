from content_scaper import scrape_new_posts, preproccess_url
from summarise import summarise_text
from formatter import make_body
from lemmy_poster import post
import time

import json
import newspaper
from newspaper import Article

from db import add_post

import os
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def post_event(url, title, text, summary, author, published, scraped):
    if int(os.environ["POST_REVIEW"]): return False
    if not scraped: return False

    if title.startswith("Latest news bulletin"): return False

    body = make_body(text, summary, author, published)
    x = post(title, url, body)
    if not x: return False

    logging.info("Posted")

    return True
    

# Function to be called when a new RSS item is detected
def on_new_item(feed, entry):
    scraped = True
    url = entry.link
    url = url[0] if isinstance(url, tuple) else url
    title = entry.title
    logging.info("Working on new article: {}, {}".format(url, title))

    proccessed_url, was_proccessed = preproccess_url(url)

    article = Article(proccessed_url) # only proxy the url for requesting purposes
    try:
        article.download()
    except newspaper.exceptions.ArticleBinaryDataException:
        logging.info("Failed for (ArticleBinaryDataException):", url)
        scraped = False
    try:
        article.parse()
    except newspaper.exceptions.ArticleException:
        logging.info("Failed for (ArticleException):", url)
        scraped = False

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

    if text.strip() == "":
        scraped = False
        logging.info("Could not scrape text skipping")
    else:
        logging.info("Scraped")

    if scraped:
        summary = summarise_text(text)
        logging.info("Summarised")
    else:
        summary = ""

    posted = post_event(url, title, text, summary, author, published, scraped)

    add_post(feed, url, title, author, published, text, summary, images, title_images, scraped, posted)
    logging.info("Added to db")

import click



@click.command()
@click.option('--retry', is_flag=True, help='retry posts with errors')
def main(retry):
    while True:
        # scrape new items without retrying failed scrapes
        scrape_new_posts(on_new_item, True)
        time.sleep(10)

if __name__ == "__main__":
    main()