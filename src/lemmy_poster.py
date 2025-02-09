from pythorhead import Lemmy
import os


lemmy = Lemmy(os.environ["LEMMY_INSTANCE"], request_timeout=10)
a = lemmy.log_in(os.environ["LEMMY_USERNAME"], os.environ["LEMMY_PASSWORD"])


community_id = lemmy.discover_community(os.environ["LEMMY_COMMUNITY"])


def post(title, url, body):
    return lemmy.post.create(community_id, title, url=url, body=body)
