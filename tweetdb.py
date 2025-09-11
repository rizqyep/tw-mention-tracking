import sqlite3
import time
import json
import os

DB_PATH = os.getenv("TWEET_DB_PATH", "tweet.db")


class DB:
    def __init__(self):
        # Ensure the directory exists before creating the database
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.setup_database()

    def connect(self):
        return sqlite3.connect(DB_PATH)

    def setup_database(self):
        """Initialize the database and create necessary tables."""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute(
                """CREATE TABLE IF NOT EXISTS replied_tweets
                         (tweet_id VARCHAR(255))"""
            )
            conn.commit()

    def store_replied_tweet_id(self, tweet_id: str):
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO replied_tweets (tweet_id) VALUES (?)", (tweet_id,))
            conn.commit()

    def get_replied_tweet_id(self):
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT tweet_id FROM replied_tweets")
            return c.fetchall()

    def get_replied_tweet_id_by_tweet_id(self, tweet_id: str):
        with self.connect() as conn:
            c = conn.cursor()
            c.execute(
                "SELECT tweet_id FROM replied_tweets WHERE tweet_id = ?", (tweet_id,)
            )
            return c.fetchone()
