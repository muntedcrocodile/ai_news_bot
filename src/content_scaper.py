import os
import sys

import feedparser
import time
from db import has_seen_item, get_feeds, add_feed
import urllib.parse
from datetime import datetime

from playwright.sync_api import sync_playwright
from newspaper import article as Article

import shutil

import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)



# checks if a url is a nytimes url and proxy it to bypass paywall
def preproccess_url(url):
    if not (urllib.parse.urlparse(url).netloc == "www.nytimes.com" or urllib.parse.urlparse(url).netloc == "nytimes.com"):
        return url, False

    current_time = datetime.now()
    timestamp = current_time.strftime("%Y%m%d%H%M%S")

    base_url = "https://archive.md/{}/".format(timestamp)
    return base_url + urllib.parse.quote(url, safe=':\/'), True


# remove duplicates and simplifications
def proccess_authors(authors: list) -> list:
    out = dict()

    for j in authors:
        key = j.lower().replace(" ", "-")
        if key in out.keys(): continue
        out[key] = j
    return ", ".join(out.values())

# makes a new profile from a profile template
def make_profile(template_dir, profile_dir):
    # delete existing contents of profile_dir
    try:
        shutil.rmtree(profile_dir)
    except FileNotFoundError:
        pass # dont need to remove file since it doesnt exist
    # copy template data to profile_dir
    shutil.copytree(template_dir, profile_dir, dirs_exist_ok=True)


def scrape_content(url):
    with sync_playwright() as p:
    
        # make browser and get a page to work with
        browser = p.firefox.launch_persistent_context(headless=True, user_data_dir="./data/profile")
        page = browser.pages[0]

        
        page.goto(url)

        article = Article(url, input_html=page.content())
        article.parse()

        return article.title, article.text, article.images, article.authors, article.publish_date


def scrape_new_posts(callback, retry=False):
    for feed in get_feeds():
        parsed_feed = feedparser.parse(feed)

        # Check if the feed was successfully parsed
        try:
            if parsed_feed.status != 200:
                logging.info(f"Error parsing feed {feed}: {parsed_feed.status}")
                continue
        except ValueError:
            logging.info(f"Error parsing feed {feed}: {parsed_feed.status}")
            continue

        # Get the latest items in the feed
        for entry in parsed_feed.entries:
            if has_seen_item(feed, entry.link, retry):
                continue
            callback(feed, entry)