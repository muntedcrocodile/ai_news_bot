from db import add_feed

import click
import feedparser
import sys
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def validate_rss_feed(rss):
    """Validate if the provided RSS feed is valid"""
    try:
        feed = feedparser.parse(rss)
        if feed.feed:
            return True
        else:
            return False
    except Exception as e:
        logging.info(f"Error validating RSS feed: {e}")
        return False

@click.command()
@click.option("--rss", prompt="RSS feed URL", help="The URL of the RSS feed")
@click.option("--name", prompt="Human-readable name", help="A human-readable name for the RSS feed")
def add_rss_feed(rss, name):
    """Add an RSS feed with a human-readable name"""
    if validate_rss_feed(rss):
        logging.info(f"Adding RSS feed '{rss}' with name '{name}'")
        add_feed(rss, name)
    else:
        logging.info("Invalid RSS feed. Please try again.")

if __name__ == "__main__":
    add_rss_feed()