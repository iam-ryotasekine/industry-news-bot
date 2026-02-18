import feedparser
import urllib.parse
import datetime

KEYWORD = "AIエージェント"
safe_keyword = urllib.parse.quote(KEYWORD)
RSS_URL = "https://news.google.com/rss/search?q=" + safe_keyword + "&hl=ja&gl=JP&ceid=JP:ja"

def generate_markdown_report():
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    feed = feedparser.parse(RSS_URL)

    with open("news_report.md", "w", encoding="utf-8") as f:
        f.write("# 🤖 【" + today + "】" + KEYWORD + " 最新ニュース\n\n")

        for entry in feed.entries[:5]:
            f.write("### [" + entry.title + "](" + entry.link + ")\n")
            f.write("- 公開日時: " + entry.get('published', '日時不明') + "\n\n")

    print("✅ ニュースレポート（news_report.md）の作成が完了しました！")

if __name__ == "__main__":
    generate_markdown_report()