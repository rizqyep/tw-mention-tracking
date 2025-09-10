import sqlite3
import time
import json

DB_PATH = "oauth.db"


class DB:
    def __init__(self):
        self.setup_database()

    def connect(self):
        return sqlite3.connect(DB_PATH)

    def setup_database(self):
        """Initialize the database and create necessary tables."""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS oauth_tokens
                         (token TEXT, expires_at REAL, refresh_token TEXT)''')
            conn.commit()

    def store_token(self, token):
        """Store OAuth token and expiration in the database."""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM oauth_tokens")
            c.execute("INSERT INTO oauth_tokens \
                      (token, expires_at, refresh_token) VALUES (?, ?, ?)",
                      (json.dumps(token), token["expires_at"],
                       token["refresh_token"]))
            conn.commit()

    def get_token(self):
        """Retrieve the latest OAuth token from the database."""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT token FROM oauth_tokens \
                       ORDER BY expires_at DESC LIMIT 1")
            row = c.fetchone()
            return json.loads(row[0]) if row else None

    def is_token_valid(self):
        """Check if the current token is valid."""
        token = self.get_token()
        if not token:
            return False
        return time.time() < token.get("expires_at", 0)

    def get_refresh_token(self):
        """Retrieve the refresh token."""
        with self.connect() as conn:
            c = conn.cursor()
            c.execute("SELECT refresh_token FROM oauth_tokens \
                      ORDER BY expires_at DESC LIMIT 1")
            row = c.fetchone()
            return row[0] if row else None
