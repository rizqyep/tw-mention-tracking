#!/usr/bin/env python3
"""
Python-based scheduler for mention tracking
Uses the schedule library to run tasks at regular intervals
"""
import schedule
import time
import asyncio
from datetime import datetime
from pathlib import Path
import sys

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the main functions
from rapidapi import track_mention_and_reply
import tweetdb


def run_mention_tracking():
    """Run the mention tracking system with proper error handling"""
    try:
        print("Starting mention tracking job")

        # Initialize database
        tdb = tweetdb.DB()
        tdb.setup_database()

        # Run the main function with the X client
        asyncio.run(track_mention_and_reply())

        print("Mention tracking job completed successfully")

    except Exception as e:
        print(f"Mention tracking job failed: {str(e)}")


def main():
    """Main scheduler function"""
    print("Starting mention tracking scheduler")

    # Schedule the job to run every 5 minutes
    schedule.every(30).seconds.do(run_mention_tracking)

    # Alternative schedules you can use:
    # schedule.every(1).minutes.do(run_mention_tracking)  # Every minute
    # schedule.every(10).minutes.do(run_mention_tracking)  # Every 10 minutes
    # schedule.every().hour.do(run_mention_tracking)       # Every hour
    # schedule.every().day.at("09:00").do(run_mention_tracking)  # Daily at 9 AM
    # schedule.every().monday.do(run_mention_tracking)     # Every Monday

    print("Scheduler configured to run every 1 minute")
    print("Press Ctrl+C to stop the scheduler")

    # Run the scheduler
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # Check every second
    except KeyboardInterrupt:
        print("Scheduler stopped by user")
    except Exception as e:
        print(f"Scheduler error: {str(e)}")


if __name__ == "__main__":
    main()
