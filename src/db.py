from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

import os


engine = create_engine(os.environ["DATABASE_URI"])
Base = declarative_base()

class SeenItem(Base):
    __tablename__ = 'seen_items'
    id = Column(Integer, primary_key=True)
    feed_url = Column(String, ForeignKey('feeds.url'))
    url = Column(String)
    title = Column(String)
    authors = Column(String)
    published = Column(DateTime)
    text = Column(String)
    images = Column(String)
    title_images = Column(String)
    summary = Column(String, default="")
    posted = Column(Boolean, default=False)

class Feed(Base):
    __tablename__ = 'feeds'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_seen_item(feed_url, url, title, authors, published, text, summary, images, title_images, posted):
    feed = session.query(Feed).filter_by(url=feed_url).first()
    if feed:
        new_item = SeenItem(
            feed_url=feed_url,
            url=url,
            title=title,
            authors=authors,
            published=published,
            text=text,
            summary=summary,
            images=images,
            title_images=title_images,
            posted=posted
            )
        session.add(new_item)
        session.commit()

def has_seen_item(feed_url, url):
    existing_item = session.query(SeenItem).filter_by(feed_url=feed_url, url=url).first()
    return existing_item is not None

def add_feed(url, name):
    existing_feed = session.query(Feed).filter_by(url=url).first()
    if not existing_feed:
        new_feed = Feed(url=url, name=name)
        session.add(new_feed)
        session.commit()

def get_feeds():
    return [feed.url for feed in session.query(Feed).all()]

def get_unposted_items():
    return session.query(SeenItem).filter_by(posted=False).with_entities(
        SeenItem.id,
        SeenItem.title,
        SeenItem.url,
        SeenItem.text,
        SeenItem.summary,
        SeenItem.authors,
        SeenItem.published
    ).all()

def mark_posted(item_id):
    item = session.query(SeenItem).get(item_id)
    if item:
        item.posted = True
        session.commit()
        return True
    return False