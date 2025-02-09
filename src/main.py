from content_scaper import scrape_new_posts, preproccess_url, make_profile, scrape_content, proccess_authors
from summarise import summarise_text
from formatter import make_body
from lemmy_poster import post
import time

import json
import newspaper

from db import add_post

import os
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def post_event(url, title, text, summary, author, published, scraped):
    if int(os.environ["POST_REVIEW"]): return False
    if not scraped: return False

    if title.startswith("Latest news bulletin"): return False
    if len(text) < 200: return False

    body = make_body(text, summary, author, published)
    x = post(title, url, body)
    logging.info("Url: {}\ntitle: {}\nStatus: {}".format(url, title, str(x)))
    if not x: return False

    logging.info("Posted")

    return True
    

# Function to be called when a new RSS item is detected
def on_new_item(feed, entry):
    scraped = True
    url = entry.link
    url = url[0] if isinstance(url, tuple) else url
    rss_title = entry.title
    logging.info("Working on new article: {}, {}".format(url, rss_title))

    proccessed_url, was_proccessed = preproccess_url(url)


    content_title = ""
    text = ""
    content_authors = []
    published = ""
    try:
        content_title, text, images, content_authors, published = scrape_content(proccessed_url)
    except Exception as e:
        logging.error("Failed for: {}".format(url), exc_info=True)
        scraped = False

    try:
        rss_author = entry.author
    except AttributeError:
        rss_author = ""

    images = json.dumps(images)
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

    # use fallbacks as nessasary
    author = rss_author
    if author.strip() == "":
        author = proccess_authors(content_authors)
    if author.strip() == "":
        author = "Unknown"
    
    title = rss_title
    if title.strip() == "":
        title = content_title
    if author.strip() == "":
        title = "Unknown"

    posted = post_event(url, title, text, summary, author, published, scraped)

    add_post(feed, url, title, author, published, text, summary, images, title_images, scraped, posted)
    logging.info("Added to db")

import click



@click.command()
@click.option('--retry', is_flag=True, help='retry posts with errors')
def main(retry):
    # make a playwrite profile to use for content scraping
    make_profile("./profile_template", "./data/profile")

    while True:
        # scrape new items without retrying failed scrapes
        scrape_new_posts(on_new_item, retry)
        time.sleep(10)

if __name__ == "__main__":
    main()