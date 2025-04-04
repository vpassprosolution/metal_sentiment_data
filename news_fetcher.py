# ✅ FULL FIXED news_fetcher.py (with sentiment_analyzer integration)

import requests
import time
from datetime import datetime
from database import save_sentiment
from price_fetcher import fetch_price
from sentiment_analyzer import analyze_sentiment  # ✅ Added

GNEWS_API_KEY = "dd0490acae3413a8b95335a8ace58347"
GNEWS_ENDPOINT = "https://gnews.io/api/v4/search"

# 📌 Metals list with proper names
METALS = {
    "XAU": "gold",
    "XAG": "silver",
    "XCU": "copper",
    "XPT": "platinum",
    "XPD": "palladium",
    "ALU": "aluminum",
    "ZNC": "zinc",
    "NI": "nickel",
    "TIN": "tin",
    "LEAD": "lead"
}

# 📌 Smart financial keywords filter
FINANCIAL_KEYWORDS = [
    "price", "rise", "fall", "forecast", "trend", "market", "trading", "demand",
    "supply", "investor", "inflation", "recession", "tariff", "rate", "economy",
    "bullish", "bearish", "resistance", "support", "fundamentals", "technical"
]

import re
KEYWORD_PATTERN = re.compile(r'\b(?:' + '|'.join(FINANCIAL_KEYWORDS) + r')\b', re.IGNORECASE)

def is_relevant_article(article):
    combined_text = f"{article['title']} {article.get('description', '')}"
    return bool(KEYWORD_PATTERN.search(combined_text))

def fetch_news(metal_name):
    query = f"{metal_name} price OR {metal_name} market"
    params = {
        "q": query,
        "token": GNEWS_API_KEY,
        "lang": "en",
        "max": 10,
        "sortby": "publishedAt"
    }
    response = requests.get(GNEWS_ENDPOINT, params=params)
    data = response.json()
    articles = data.get("articles", [])

    # ✅ Filter top 3 financial articles
    relevant_articles = [
        {
            "title": a["title"],
            "sentiment": "",  # optional sentiment logic later
            "summary": a.get("description", "")
        }
        for a in articles if is_relevant_article(a)
    ][:3]

    return relevant_articles

def process_news(symbol, metal_name):
    print(f"\n📰 Fetching news for {symbol} ({metal_name})...")
    articles = fetch_news(metal_name)

    if len(articles) < 3:
        print(f"❌ Not enough good news for {symbol}. Skipping update.")
        return

    print(f"✅ 3 articles found for {symbol} ({metal_name})")
    price = fetch_price(symbol)

    # ✅ Use the new analyzer
    sentiment, recommendation, articles = analyze_sentiment(articles)

    save_sentiment(symbol, price, sentiment, recommendation, articles)
    print(f"✅ {symbol} saved to database")

def run_sentiment_update():
    print("\n🔁 Running metal sentiment updater...")
    for symbol, metal_name in METALS.items():
        try:
            process_news(symbol, metal_name)
            time.sleep(1)  # polite pause
        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")

# ✅ Add this at bottom of news_fetcher.py
def fetch_articles(symbol):
    metal_name = METALS.get(symbol, "")
    if not metal_name:
        return []
    return fetch_news(metal_name)

if __name__ == "__main__":
    run_sentiment_update()
