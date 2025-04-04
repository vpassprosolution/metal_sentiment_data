import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from price_fetcher import fetch_price
from news_fetcher import fetch_articles
from sentiment_analyzer import analyze_sentiment
from database import save_sentiment

# ✅ Metals we track
METALS = ["XAU", "XAG", "XCU", "XPT", "XPD", "ALU", "ZNC", "NI", "TIN", "LEAD"]

async def run_sentiment_update():
    print("\n🔁 Running metal sentiment updater...\n")

    for symbol in METALS:
        print(f"📰 Fetching news for {symbol}...")

        # Step 1: Fetch news articles
        articles = await fetch_articles(symbol)
        if len(articles) < 3:
            print(f"❌ Not enough good news for {symbol}. Skipping update.\n")
            continue

        # Step 2: Fetch price
        price = await fetch_price(symbol)
        if price is None:
            print(f"❌ Failed to get price for {symbol}. Skipping.\n")
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

        print(f"✅ {symbol} saved to database\n")

    print("✅ All metals processed.\n")

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_sentiment_update, "interval", hours=4)  # Run every 4 hours
    scheduler.start()
    print("🕓 Scheduler started (every 4 hours)")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    start_scheduler()
    loop.run_forever()
