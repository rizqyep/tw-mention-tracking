#!/usr/bin/env python3
"""
Advanced Python-based scheduler for mention tracking
Includes multiple scheduling options and better error handling
"""
import schedule
import time
import asyncio
import logging
import threading
from datetime import datetime, timedelta
from pathlib import Path
import sys
import signal

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import the main functions
from main import track_mention_and_reply, X
import tweetdb

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("mention_tracking.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class MentionTrackerScheduler:
    def __init__(self):
        self.running = True
        self.job_count = 0
        self.last_run = None

    def run_mention_tracking(self):
        """Run the mention tracking system with proper error handling"""
        try:
            self.job_count += 1
            logger.info(f"Starting mention tracking job #{self.job_count}")

            # Initialize database
            tdb = tweetdb.DB()
            tdb.setup_database()

            # Initialize X API client
            x = X()

            # Run the main function with the X client
            asyncio.run(track_mention_and_reply(x))

            self.last_run = datetime.now()
            logger.info(
                f"Mention tracking job #{self.job_count} completed successfully"
            )

        except Exception as e:
            logger.error(f"Mention tracking job #{self.job_count} failed: {str(e)}")

    def setup_schedules(self):
        """Setup different scheduling options"""

        # Option 1: Every 5 minutes
        schedule.every(5).minutes.do(self.run_mention_tracking)

        # Option 2: Every 10 minutes (uncomment to use)
        # schedule.every(10).minutes.do(self.run_mention_tracking)

        # Option 3: Every hour (uncomment to use)
        # schedule.every().hour.do(self.run_mention_tracking)

        # Option 4: Every day at specific times (uncomment to use)
        # schedule.every().day.at("09:00").do(self.run_mention_tracking)
        # schedule.every().day.at("15:00").do(self.run_mention_tracking)
        # schedule.every().day.at("21:00").do(self.run_mention_tracking)

        # Option 5: Every weekday at 9 AM (uncomment to use)
        # schedule.every().monday.at("09:00").do(self.run_mention_tracking)
        # schedule.every().tuesday.at("09:00").do(self.run_mention_tracking)
        # schedule.every().wednesday.at("09:00").do(self.run_mention_tracking)
        # schedule.every().thursday.at("09:00").do(self.run_mention_tracking)
        # schedule.every().friday.at("09:00").do(self.run_mention_tracking)

        logger.info("Schedules configured:")
        for job in schedule.jobs:
            logger.info(f"  - {job}")

    def run_scheduler(self):
        """Run the scheduler in a separate thread"""
        logger.info("Starting scheduler thread")
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(1)  # Check every second
            except Exception as e:
                logger.error(f"Scheduler error: {str(e)}")
                time.sleep(5)  # Wait 5 seconds before retrying

    def start(self):
        """Start the scheduler"""
        logger.info("Starting mention tracking scheduler")
        self.setup_schedules()

        # Start scheduler in a separate thread
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()

        logger.info("Scheduler started. Press Ctrl+C to stop.")

        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Received interrupt signal")
            self.stop()

    def stop(self):
        """Stop the scheduler"""
        logger.info("Stopping scheduler...")
        self.running = False
        schedule.clear()
        logger.info("Scheduler stopped")

    def status(self):
        """Print scheduler status"""
        print(f"Scheduler running: {self.running}")
        print(f"Jobs completed: {self.job_count}")
        print(f"Last run: {self.last_run}")
        print(f"Scheduled jobs: {len(schedule.jobs)}")
        for job in schedule.jobs:
            print(f"  - {job}")


def signal_handler(signum, frame):
    """Handle interrupt signals"""
    logger.info("Received signal, stopping scheduler...")
    scheduler.stop()
    sys.exit(0)


if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create and start scheduler
    scheduler = MentionTrackerScheduler()
    scheduler.start()
