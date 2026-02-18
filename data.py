import feedparser
import urllib.parse

KEYWORD = "AIエージェント"

safe_keyword = urllib.parse.quote(KEYWORD)
RSS_URL = "https://news.google.com/rss/search?q=" + safe_keyword + "&hl=ja&gl=JP&ceid=JP:ja"

def fetch_industry_news():
    print("📢 ニュースを取得中...")
    feed = feedparser.parse(RSS_URL)
    for entry in feed.entries[:5]:
        print("📌 " + entry.title)
        print("🔗 " + entry.link)
        print("----------------")

if __name__ == "__main__":
    fetch_industry_news()