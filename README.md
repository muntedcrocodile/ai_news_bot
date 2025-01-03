# AI News Bot
================

A bot that scrapes news articles from RSS feeds, generates AI-powered summaries, and posts the summaries and links to Lemmy.

## Overview

This bot uses Natural Language Processing (NLP) and web scraping techniques to:

1. Fetch RSS feeds from specified news sources
2. Scrape the article content from the RSS feed entries
3. Generate a concise summary of the article content using AI
4. Post the summary and link to the original article on Lemmy

## Features

* Fetches news articles from multiple RSS feed sources
* Generates AI-powered summaries of the article content
* Automatically posts summaries and links to Lemmy with Markdown formatting

## Deploy

* clone the repo 
```bash
git clone https://github.com/muntedcrocodile/ai_news_bot.git
```
* copy `.env.example` to `.env` and fill in the configuration in `.env` as required
```bash
cp .env.example .env
```
* Deploy with docker
```bash
docker compsoe up
```
* Add RSS feeds
```bash

```

## Roadmap

* Summarise all articles for the day/week/month/year to make a daily brief
* Generate argument of for and against perspective then summarise the result of the 2 arguments
* Generate embeddings to perform content grouping/simmilarity (find the missing perspectives on an issue etc) and politicla alligmnent information


## Example Use Case

1. Set up the bot to fetch RSS feeds from a popular news site
2. Run the bot to generate and post summaries to a Lemmy Community e.g. [!news_summary@lemmy.dbzer0.com](https://lemm.ee/c/news_summary@lemmy.dbzer0.com)

## Acknowledgments

This project was inspired by [LemmyAutoTldrBot](https://github.com/RikudouSage/LemmyAutoTldrBot).

## Contributing

1. Write some code
2. Make a pull request
* Toot me if you got any question [@muntedcrocodile@mastodon.social](https://mastodon.social/@muntedcrocodile)

## Donations

monero:8916FjDhEqXJqX9Koec9WaZ4QBQAa6sgW6XhQhXSjYWpQiWB42GsggEh73YAFGF86GU2gEE1TTRdWSspuMgpWGkiPHkgBTX
![monero:8916FjDhEqXJqX9Koec9WaZ4QBQAa6sgW6XhQhXSjYWpQiWB42GsggEh73YAFGF86GU2gEE1TTRdWSspuMgpWGkiPHkgBTX](https://github.com/muntedcrocodile/ai_news_bot/blob/main/static/images/muntedcrocodile_recieve.png?raw=true)