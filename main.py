import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from price_fetcher import fetch_price
from news_scraper import fetch_articles
from sentiment_analyzer import analyze_sentiment
from database import save_sentiment

# ✅ Metals we track
METALS = ["XAU", "XAG", "XCU", "XPT", "XPD", "ALU", "ZNC", "NI", "TIN", "LEAD"]

async def run_sentiment_update():
    print("🔁 Running metal sentiment updater...")

    for symbol in METALS:
        print(f"📊 Processing: {symbol}")

        # Step 1: Fetch price
        price = await fetch_price(symbol)
        if price is None:
            print(f"❌ Failed to get price for {symbol}")
            continue

        # Step 2: Fetch news articles
        articles = await fetch_articles(symbol)
        if not articles:
            print(f"⚠️ No articles found for {symbol}")
            continue

        # Step 3: Analyze sentiment
        sentiment, recommendation = analyze_sentiment(articles)

        # Step 4: Save to DB
        save_sentiment(
            symbol=symbol,
            price=price,
            sentiment=sentiment,
            recommendation=recommendation,
            article_data=articles
        )

        print(f"✅ {symbol} saved: {sentiment} ({recommendation})")

    print("✅ All metals processed.")

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_sentiment_update, "interval", hours=4)  # ⏱️ Run every 4h
    scheduler.start()
    print("🕓 Scheduler started (every 4 hours)")

if __name__ == "__main__":
    asyncio.run(run_sentiment_update())  # ← run it NOW once for testing

