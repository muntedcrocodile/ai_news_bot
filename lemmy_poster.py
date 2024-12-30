from pythorhead import Lemmy
from dotenv import load_dotenv
import os

load_dotenv()

lemmy = Lemmy(os.environ["LEMMY_INSTANCE"], request_timeout=2)
a = lemmy.log_in(os.environ["LEMMY_USERNAME"], os.environ["LEMMY_PASSWORD"])


community_id = lemmy.discover_community(os.environ["LEMMY_COMMUNITY"])


def post(title, url, body):
    lemmy.post.create(community_id, title, url=url, body=body)
