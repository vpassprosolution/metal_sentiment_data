import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from news_fetcher import fetch_articles
from price_fetcher import fetch_price
from sentiment_analyzer import analyze_sentiment
from database import save_sentiment

app = FastAPI()

# ✅ Metals we track
METALS = ["XAU", "XAG", "XCU", "XPT", "XPD", "ALU", "ZNC", "NI", "TIN", "LEAD"]

# ✅ API Endpoint to get sentiment for one metal
@app.get("/get_metal_sentiment")
async def get_metal_sentiment(symbol: str):
    if symbol not in METALS:
        return {"error": "Invalid metal symbol"}

    price = fetch_price(symbol)
    articles = fetch_articles(symbol)

    if not articles:
        return {"symbol": symbol, "price": price, "sentiment": "N/A", "recommendation": "N/A", "articles": []}

    sentiment, recommendation = analyze_sentiment(articles)

    return {
        "symbol": symbol,
        "price": price,
        "sentiment": sentiment,
        "recommendation": recommendation,
        "articles": articles
    }

# ✅ Background job
async def run_sentiment_update():
    print("🔁 Running metal sentiment updater...")
    for symbol in METALS:
        try:
            price = fetch_price(symbol)
            articles = fetch_articles(symbol)

            if not articles or len(articles) < 3:
                print(f"⚠️ Skipping {symbol} (not enough news)")
                continue

            sentiment, recommendation = analyze_sentiment(articles)
            save_sentiment(symbol, price, sentiment, recommendation, articles)
            print(f"✅ {symbol} saved")
        except Exception as e:
            print(f"❌ Error on {symbol}: {e}")

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_sentiment_update, "interval", hours=4)
    scheduler.start()
    print("🕓 Scheduler started")

@app.on_event("startup")
async def startup_event():
    start_scheduler()
    await run_sentiment_update()  # ← run once at startup

