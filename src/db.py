from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean, UniqueConstraint, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

import os


engine = create_engine(os.environ["DATABASE_URI"])
Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True)
    title = Column(String)
    authors = Column(String)
    published = Column(DateTime)
    text = Column(String)
    images = Column(String)
    title_images = Column(String)
    summary = Column(String, default="")
    scraped = Column(Boolean, default=False)
    posted = Column(Boolean, default=False)
    feed_associations = relationship("FeedAssociation", backref="post")

class Feed(Base):
    __tablename__ = 'feeds'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)
    post_associations = relationship("FeedAssociation", backref="feed")

class FeedAssociation(Base):
    __tablename__ = 'feed_associations'
    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey('feeds.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))
    __table_args__ = (UniqueConstraint('feed_id', 'post_id'),)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_post(feed_url, url, title, authors, published, text, summary, images, title_images, scraped=False, posted=False):
    existing_post = session.query(Post).filter_by(url=url).first()
    if existing_post:
        add_feed_association(existing_post, feed_url)
    else:
        new_post = Post(
            url=url,
            title=title,
            authors=authors,
            published=published,
            text=text,
            summary=summary,
            images=images,
            title_images=title_images,
            scraped=scraped,
            posted=posted
            )
        session.add(new_post)
        add_feed_association(new_post, feed_url)
    session.commit()

def has_seen_item(feed_url, url, retry: bool):
    existing_item = session.query(SeenItem).filter_by(feed_url=feed_url, url=url).first()
    if retry and existing_item and not existing_item.scraped:
        return False
    return existing_item is not None


def has_seen_item(feed_url, url, retry: bool):
    existing_post = session.query(Post).filter_by(url=url).first()

    # never seen it
    if not existing_post:
        return False

    if not existing_post.scraped and retry: # pretend we havnt seen it to retry generating it
        return False

    # add an associaation since we have got the same post again from a different feed
    add_feed_association(existing_post, feed_url)
    return True

def add_feed_association(post, feed_url):
    existing_feed = session.query(Feed).filter_by(url=feed_url).first()
    if existing_feed:
        existing_association = session.query(FeedAssociation).filter_by(feed_id=existing_feed.id, post_id=post.id).first()
        if not existing_association:
            new_association = FeedAssociation(feed=existing_feed, post=post)
            session.add(new_association)
    else:
        new_feed = Feed(url=feed_url)
        session.add(new_feed)
        new_association = FeedAssociation(feed=new_feed, post=post)
        session.add(new_association)

def add_feed(url, name):
    existing_feed = session.query(Feed).filter_by(url=url).first()
    if not existing_feed:
        new_feed = Feed(url=url, name=name)
        session.add(new_feed)
        session.commit()

def get_feeds():
    return [feed.url for feed in session.query(Feed).all()]

def get_unposted_items():
    return session.query(Post).filter_by(posted=False).with_entities(
        Post.id,
        Post.title,
        Post.url,
        Post.text,
        Post.summary,
        Post.authors,
        Post.published
    ).order_by(func.date(Post.published).asc()).all()

def mark_posted(item_id):
    item = session.query(Post).get(item_id)
    if item:
        item.posted = True
        session.commit()
        return True
    return False
