from formatter import make_body
from lemmy_poster import post
import time

from db import get_unposted_items, mark_posted

import click
import os


def main():
    for i in get_unposted_items():

        item_id, title, url, text, summary, author, published = i

        body = make_body(text, summary, author, published)

        print("="*50)
        print("ID:", item_id)
        print("Title:", title)
        print("Url:", url)
        print("Body:", body)
        print("\n\n")

        if click.confirm("Post?", default=True):
            post(title, url, body)
            mark_posted(item_id)
            print("Posted")


if __name__ == "__main__":
    while True:
        try:
            main()
            if not click.confirm("Completed! check again?", default=True):
                break
        except click.exceptions.Abort: # exit if user ctr+c
            exit()