import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime

# 🔐 Replace with your actual Railway PostgreSQL URL
DB_URL = os.getenv("DATABASE_URL", "postgresql://postgres:vVMyqWjrqgVhEnwyFifTQxkDtPjQutGb@interchange.proxy.rlwy.net:30451/railway")

def connect():
    return psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)


def save_sentiment(
    symbol,
    price,
    sentiment,
    recommendation,
    article_data
):
    conn = connect()
    cur = conn.cursor()

    now = datetime.utcnow()

    # Prepare article values
    a1 = article_data[0] if len(article_data) > 0 else {"title": "", "sentiment": "", "summary": ""}
    a2 = article_data[1] if len(article_data) > 1 else {"title": "", "sentiment": "", "summary": ""}
    a3 = article_data[2] if len(article_data) > 2 else {"title": "", "sentiment": "", "summary": ""}

    # UPSERT
    cur.execute("""
        INSERT INTO metals_sentiment (
            symbol, price, sentiment, recommendation, last_updated,
            article_1_title, article_1_sentiment, article_1_summary,
            article_2_title, article_2_sentiment, article_2_summary,
            article_3_title, article_3_sentiment, article_3_summary
        )
        VALUES (%s, %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s)
        ON CONFLICT (symbol) DO UPDATE SET
            price = EXCLUDED.price,
            sentiment = EXCLUDED.sentiment,
            recommendation = EXCLUDED.recommendation,
            last_updated = EXCLUDED.last_updated,
            article_1_title = EXCLUDED.article_1_title,
            article_1_sentiment = EXCLUDED.article_1_sentiment,
            article_1_summary = EXCLUDED.article_1_summary,
            article_2_title = EXCLUDED.article_2_title,
            article_2_sentiment = EXCLUDED.article_2_sentiment,
            article_2_summary = EXCLUDED.article_2_summary,
            article_3_title = EXCLUDED.article_3_title,
            article_3_sentiment = EXCLUDED.article_3_sentiment,
            article_3_summary = EXCLUDED.article_3_summary;
    """, (
        symbol, price, sentiment, recommendation, now,
        a1["title"], a1["sentiment"], a1["summary"],
        a2["title"], a2["sentiment"], a2["summary"],
        a3["title"], a3["sentiment"], a3["summary"]
    ))

    conn.commit()
    cur.close()
    conn.close()
