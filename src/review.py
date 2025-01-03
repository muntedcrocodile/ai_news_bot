from formatter import make_body
from lemmy_poster import post
import time

from db import get_unposted_items, mark_posted

import click
import os
import logging
import sys


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def main():
    for i in get_unposted_items():

        item_id, title, url, text, summary, author, published = i

        body = make_body(text, summary, author, published)

        logging.info("="*50)
        logging.info("ID:", item_id)
        logging.info("Title:", title)
        logging.info("Url:", url)
        logging.info("Body:", body)
        logging.info("\n\n")

        if click.confirm("Post?", default=True):
            post(title, url, body)
            mark_posted(item_id)
            logging.info("Posted")


if __name__ == "__main__":
    while True:
        try:
            main()
            if not click.confirm("Completed! check again?", default=True):
                break
        except click.exceptions.Abort: # exit if user ctr+c
            exit()