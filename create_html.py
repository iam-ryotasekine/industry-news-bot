import feedparser
from datetime import datetime, timedelta # これを追加
import urllib.parse
import datetime

KEYWORD = "AIエージェント OR 生成AI トレンド OR OCR OR RPA"
safe_keyword = urllib.parse.quote(KEYWORD)
RSS_URL = "https://news.google.com/rss/search?q=" + safe_keyword + "&hl=ja&gl=JP&ceid=JP:ja"

def format_date(date_str):
    try:
        # ニュースの日付を解析（Googleニュース等の形式）
        dt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        now = datetime.now()
        diff = now - dt

        if diff < timedelta(hours=1):
            return f"新着！ {diff.seconds // 60}分前"
        elif diff < timedelta(days=1):
            return f"今日 {dt.hour:02}:{dt.minute:02}"
        else:
            return f"{dt.month}/{dt.day}"
    except:
        return date_str # 変換に失敗したらそのまま表示
def get_source_info(source_name):
    # ソース名に含まれる文字で色とアイコンを判定
    if "Google" in source_name:
        return "🌐", "#4285f4" # Googleブルー
    elif "PR TIMES" in source_name:
        return "📢", "#0b419b" # PR TIMESネイビー
    elif "Tech" in source_name:
        return "💻", "#ff4500" # テック系オレンジ
    elif "Zenn" in source_name or "Qiita" in source_name:
        return "🤓", "#2ea44f" # 技術記事グリーン
    else:
        return "📰", "#6b7280" # その他グレー
def get_ai_summary_demo(title):
    # APIキーが使えるようになるまでの「デモ用」の要約枠
    return f"""
    <div class='ai-summary'>
        <div class='ai-summary-title'>✨ Gemini AI 要約 (Demo)</div>
        <ul>
            <li>この記事「{title[:20]}...」の重要ポイントをAIが解析中。</li>
            <li>APIキー設定完了後、ここに3行要約が自動生成されます。</li>
            <li>社内展開時のイメージとして先行実装しています。</li>
        </ul>
    </div>
    """
def generate_html_dashboard():
    today = datetime.datetime.now().strftime("%Y年%m月%d日")
    feed = feedparser.parse(RSS_URL)
    html_text = "<!DOCTYPE html>\n<html lang='ja'>\n<head>\n"
    html_text += "<meta charset='UTF-8'>\n"
    html_text += "<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
    html_text += f"<title>🤖 {today} AIトレンド・ダッシュボード</title>\n"
    html_text += "<link href='https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap' rel='stylesheet'>\n"
    html_text += "<style>\n"
    html_text += "    .ai-summary { background-color: #f8fafc; border-left: 4px solid #667eea; padding: 12px; margin: 10px 0; font-size: 14px; border-radius: 0 8px 8px 0; }\n"
    html_text += "    .ai-summary-title { font-weight: bold; color: #4a5568; margin-bottom: 5px; display: flex; align-items: center; gap: 5px; }\n"
    html_text += "    .ai-summary ul { margin: 0; padding-left: 20px; color: #4a5568; }\n"
    html_text += "    .ai-summary li { margin-bottom: 3px; }\n"
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
    html_text += "#backToTop {\n"
    html_text += "display: none; position: fixed; bottom: 20px; right: 20px;\n"
    html_text += "background-color: #667eea; color: white; border: none;\n"
    html_text += "padding: 15px; border-radius: 50%; cursor: pointer; font-size: 18px;\n"
    html_text += "box-shadow: 0 4px 8px rgba(0,0,0,0.2); z-index: 99;\n"
    html_text += "}\n"
    html_text += "</style>\n</head>\n<body>\n"
    html_text += "<div class='header'>\n"
    html_text += '<button onclick="topFunction()" id="backToTop" title="Go to top">▲</button>\n'
    html_text += """
        <script>
        let mybutton = document.getElementById("backToTop");
        window.onscroll = function() {
            if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
                mybutton.style.display = "block";
            } else {
                mybutton.style.display = "none";
            }
        };
        function topFunction() {
            window.scrollTo({top: 0, behavior: 'smooth'});
        }
        </script>
        """
    for entry in feed.entries[:15]:
        display_date = format_date(entry.get('published', ''))
        source = entry.get('source', {}).get('title', '不明')
        icon, color = get_source_info(source)
        summary_html = get_ai_summary_demo(entry.title)       
        html_text += f"<div class='card'>\n"
        html_text += f"    <span class='source-badge' style='background-color: {color};'>{icon} {source}</span>\n"
        html_text += f"    <a href='{entry.link}' target='_blank'>{entry.title}</a>\n"
        html_text += f"    {summary_html}\n"
        html_text += f"    <div class='date'>🕒 {display_date}</div>\n"
        html_text += f"    </div>\n"
    html_text += "     </body>\n</html>"

    with open("news_dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_text)

    print("✨ おしゃれなニュースダッシュボードに進化しました！")

if __name__ == "__main__":
    generate_html_dashboard()