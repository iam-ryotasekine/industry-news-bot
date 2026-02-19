import feedparser
import urllib.parse
import datetime

KEYWORD = "AIエージェント 最新"
safe_keyword = urllib.parse.quote(KEYWORD)
RSS_URL = "https://news.google.com/rss/search?q=" + safe_keyword + "&hl=ja&gl=JP&ceid=JP:ja"

def generate_html_dashboard():
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    feed = feedparser.parse(RSS_URL)
    # 修正イメージ
    for entry in feed.entries:
     title = entry.title
     link = entry.link
     # タイトルの後ろにある「 - 媒体名」を切り離して取得
     source = entry.get('source', {}).get('title', '不明')

    html_text = "<!DOCTYPE html>\n<html lang='ja'>\n<head>\n"
    html_text += "<meta charset='UTF-8'>\n"
    html_text += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
    html_text += "<title>🤖 AIトレンド・ダッシュボード | Ryota's Bot</title>\n"
    html_text += "<link href='https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap' rel='stylesheet'>\n"
    html_text += "<style>\n"
    html_text += "body { font-family: 'Noto Sans JP', sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 0; }\n"
    html_text += ".container { max-width: 800px; margin: 0 auto; padding: 20px; }\n"
    html_text += ".header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; text-align: center; border-radius: 0 0 15px 15px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }\n"
    html_text += f'<div class="header">\n'
    html_text += f'<h1>🤖 AI業界ニュース・ダッシュボード</h1>\n'
    html_text += f'<p class="status-tag">● 自動更新稼働中</p>\n'
    html_text += f'<p class="update-time">最終更新:{today}</p>\n'
    html_text += f'</div>\n'
    html_text += ".header p { margin: 10px 0 0 0; opacity: 0.9; font-size: 14px; }\n"
    html_text += ".card { background: white; padding: 20px; margin-bottom: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); transition: transform 0.2s, box-shadow 0.2s; border-left: 5px solid #667eea; }\n"
    html_text += ".card:hover { transform: translateY(-3px); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }\n"
    html_text += "a { color: #2d3748; text-decoration: none; font-size: 18px; font-weight: 700; display: block; margin-bottom: 8px; line-height: 1.4; }\n"
    html_text += "a:hover { color: #667eea; }\n"
    html_text += ".date { color: #a0aec0; font-size: 13px; }\n"
    html_text += ".source-badge {background-color: #e0e7ff; /* 清潔感のある薄い青 */color: #4338ca;/* 視認性の良い濃い青 */padding: 4px 10px;border-radius: 20px;       /* 角を丸めてモダンな印象に */font-size: 11px;font-weight: bold;margin-bottom: 10px;display: inline-block;     /* これでタグっぽくなります */}"
    html_text += "</style>\n</head>\n<body>\n"
    html_text += "<div class='header'>\n"
    html_text += f'<span class="source-badge">{source}</span>\n'
    html_text += f'<a href="{link}" target="_blank">{title}</a>\n'
    for entry in feed.entries[:5]:
        html_text += "<div class='card'>\n"
        html_text += "<a href='" + entry.link + "' target='_blank'>" + entry.title + "</a>\n"
        html_text += "<div class='date'>🕒 " + entry.get('published', '日時不明') + "</div>\n"
        html_text += "</div>\n"

    html_text += "</div>\n"
    html_text += "</body>\n</html>"

    with open("news_dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_text)

    print("✨ おしゃれなニュースダッシュボードに進化しました！")

if __name__ == "__main__":
    generate_html_dashboard()