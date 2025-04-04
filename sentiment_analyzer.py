# sentiment_analyzer.py

def analyze_sentiment(articles):
    sentiment_score = 0
    analyzed_articles = []

    # Define basic sentiment keywords
    positive_words = ["rise", "bullish", "positive", "jump", "growth", "gain", "demand", "up", "buy"]
    negative_words = ["fall", "bearish", "drop", "crash", "decline", "down", "sell", "fear", "recession"]

    for article in articles:
        title = article["title"].lower()
        summary = article["summary"].lower()
        content = f"{title} {summary}"

        score = 0
        for word in positive_words:
            if word in content:
                score += 1
        for word in negative_words:
            if word in content:
                score -= 1

        # Add to total score
        sentiment_score += score

        # Determine individual article sentiment
        if score > 0:
            sentiment = "Bullish"
        elif score < 0:
            sentiment = "Bearish"
        else:
            sentiment = "Neutral"

        analyzed_articles.append({
            "title": article["title"],
            "summary": article["summary"],
            "sentiment": sentiment
        })

    # Final overall sentiment
    if sentiment_score >= 2:
        overall_sentiment = "Bullish"
        recommendation = "BUY"
    elif sentiment_score <= -2:
        overall_sentiment = "Bearish"
        recommendation = "SELL"
    else:
        overall_sentiment = "Neutral"
        recommendation = "NEUTRAL"

    return overall_sentiment, recommendation, analyzed_articles
