import feedparser
from datetime import datetime, timedelta
import urllib.parse

# --- 設定エリア ---
KEYWORD = "AIエージェント OR 生成AI トレンド OR OCR OR RPA"
RSS_URL = "https://news.google.com/rss/search?q=" + urllib.parse.quote(KEYWORD) + "&hl=ja&gl=JP&ceid=JP:ja"

def format_date(date_str):
    try:
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
        return date_str

def get_source_info(source_name):
    if "Google" in source_name: return "🌐", "#4285f4"
    elif "PR TIMES" in source_name: return "📢", "#0b419b"
    elif "Tech" in source_name: return "💻", "#ff4500"
    elif "Zenn" in source_name or "Qiita" in source_name: return "🤓", "#2ea44f"
    else: return "📰", "#6b7280"

def calculate_scoring(title):
    score = 0
    if "AI" in title or "人工知能" in title: score += 2
    if "SaaS" in title or "クラウド" in title: score += 1
    if "営業" in title or "セールス" in title: score += 1
    
    if score > 0:
        return f"<span style='color: #f39c12; margin-left: 8px; font-size: 22px;'>{'★' * score}</span>"
    return ""

def get_category_tag(title):
    """【タグ増量版】タイトルからカテゴリを自動判定してタグを生成"""
    if "営業" in title or "セールス" in title:
        return "<span class='category-tag tag-sales'>💰 Sales</span>"
    elif "SaaS" in title or "クラウド" in title:
        return "<span class='category-tag tag-saas'>☁️ SaaS/Cloud</span>"
    elif "自動化" in title or "RPA" in title or "DX" in title:
        return "<span class='category-tag tag-dx'>⚡ DX/Automation</span>"
    elif "AI" in title or "生成" in title or "人工知能" in title:
        return "<span class='category-tag tag-ai'>🤖 AI/Tech</span>"
    else:
        return "<span class='category-tag tag-gen'>📰 General</span>"

def get_ai_summary_demo(title):
    return f"""
    <div class='ai-summary'>
        <div class='ai-summary-title'>✨ Gemini AI 要約 (Demo)</div>
        <ul>
            <li>この記事「{title[:20]}...」の重要ポイントをAIが解析中。</li>
            <li>APIキー設定完了後、ここに3行要約が自動生成されます。</li>
        </ul>
    </div>
    """

def get_html_style():
    """【タグ増量版】新しいタグの配色（CSS）を追加"""
    return """
    <style>
        body { font-family: 'Noto Sans JP', sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 0; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; text-align: center; border-radius: 0 0 15px 15px; margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .card { background: white; padding: 20px; margin-bottom: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #667eea; }
        a { color: #2d3748; text-decoration: none; font-size: 18px; font-weight: 700; display: block; margin-bottom: 8px; }
        .date { color: #a0aec0; font-size: 13px; margin-top: 10px; }
        .source-badge { color: white; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: bold; margin-bottom: 10px; display: inline-block; }
        .ai-summary { background-color: #f8fafc; border-left: 4px solid #667eea; padding: 12px; margin: 10px 0; font-size: 14px; border-radius: 0 8px 8px 0; }
        
        /* カテゴリタグ用のスタイル */
        .category-tag { padding: 3px 8px; border-radius: 5px; font-size: 10px; font-weight: bold; margin-right: 5px; vertical-align: middle; }
        .tag-sales { background-color: #fff3e0; color: #e65100; }
        .tag-ai { background-color: #f3e5f5; color: #4a148c; }
        .tag-saas { background-color: #e3f2fd; color: #1565c0; } 
        .tag-dx { background-color: #e8f5e9; color: #2e7d32; }   
        .tag-gen { background-color: #f5f5f5; color: #616161; }
    </style>
    """

def generate_html_dashboard():
    today = datetime.now().strftime("%Y年%m月%d日")
    feed = feedparser.parse(RSS_URL)
    
    html_text = f"""<!DOCTYPE html>
    <html lang='ja'>
    <head>
        <meta charset='UTF-8'>
        <title>🤖 {today} AIダッシュボード</title>
        <link href='https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap' rel='stylesheet'>
        {get_html_style()}
    </head>
    <body>
        <div class='header'>
            <h1>🤖 AI業界ニュース・ダッシュボード</h1>
            <p>最終更新: {today}</p>
        </div>
        <div class='container'>
    """

    for entry in feed.entries[:15]:
        display_date = format_date(entry.get('published', ''))
        source = entry.get('source', {}).get('title', '不明')
        icon, color = get_source_info(source)
        
        stars = calculate_scoring(entry.title)
        category_tag = get_category_tag(entry.title)
        summary_html = get_ai_summary_demo(entry.title)
        
        html_text += f"""
        <div class='card'>
            <div style='margin-bottom: 8px;'>
                {category_tag}
                <span class='source-badge' style='background-color: {color};'>{icon} {source}</span>
            </div>
            <a href='{entry.link}' target='_blank'>{entry.title}{stars}</a>
            {summary_html}
            <div class='date'>🕒 {display_date}</div>
        </div>
        """

    html_text += "</div></body></html>"

    with open("news_dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_text)
    print("✨ カテゴリタグ増量版のダッシュボードに進化しました！")

if __name__ == "__main__":
    generate_html_dashboard()