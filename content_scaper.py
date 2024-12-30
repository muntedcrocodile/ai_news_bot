import os

import feedparser
import time
from db import has_seen_item, get_feeds, add_feed
import urllib.parse
from datetime import datetime

# # testing
# add_feed("https://rss.nytimes.com/services/xml/rss/nyt/World.xml", "NY Times: World - World")


# checks if a url is a nytimes url and proxy it to bypass paywall
def preproccess_url(url):
    if not (urllib.parse.urlparse(url).netloc == "www.nytimes.com" or urllib.parse.urlparse(url).netloc == "nytimes.com"):
        return url

    current_time = datetime.now()
    timestamp = current_time.strftime("%Y%m%d%H%M%S")

    base_url = "https://archive.md/{}/".format(timestamp)
    return base_url + urllib.parse.quote(url, safe=':\/')


# remove duplicates and simplifications
def proccess_authors(authors: list):
    out = dict()

    for j in authors:
        key = j.lower().replace(" ", "-")
        if key in out.keys(): continue
        out[key] = j

def scrape_new_posts(callback):
    for feed in get_feeds():
        parsed_feed = feedparser.parse(feed)

        # Check if the feed was successfully parsed
        if parsed_feed.status != 200:
            print(f"Error parsing feed {feed}: {parsed_feed.status}")
            continue

        # Get the latest items in the feed
        for entry in parsed_feed.entries:
            if has_seen_item(feed, entry.link):
                continue
            callback(feed, entry)