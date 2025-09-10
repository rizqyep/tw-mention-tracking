# Python Scheduler for Mention Tracking

This directory contains Python-based schedulers to run the mention tracking system at regular intervals.

## Files

- `scheduler.py` - Simple scheduler using the `schedule` library
- `advanced_scheduler.py` - Advanced scheduler with better error handling and multiple options
- `run_cron.py` - Single-run script for external cron jobs

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Simple Scheduler (Recommended)

Run the simple scheduler that checks for mentions every 5 minutes:

```bash
python3 scheduler.py
```

### Advanced Scheduler

Run the advanced scheduler with more options:

```bash
python3 advanced_scheduler.py
```

### Single Run (for external cron)

Run once and exit:

```bash
python3 run_cron.py
```

## Scheduling Options

You can modify the scheduling in `scheduler.py` or `advanced_scheduler.py`:

```python
# Every minute
schedule.every(1).minutes.do(run_mention_tracking)

# Every 5 minutes (default)
schedule.every(5).minutes.do(run_mention_tracking)

# Every 10 minutes
schedule.every(10).minutes.do(run_mention_tracking)

# Every hour
schedule.every().hour.do(run_mention_tracking)

# Every day at 9 AM
schedule.every().day.at("09:00").do(run_mention_tracking)

# Every weekday at 9 AM
schedule.every().monday.at("09:00").do(run_mention_tracking)
```

## Running in Background

### Using nohup (Linux/Mac)

```bash
nohup python3 scheduler.py > scheduler.log 2>&1 &
```

### Using screen (Linux/Mac)

```bash
screen -S mention_tracker
python3 scheduler.py
# Press Ctrl+A then D to detach
```

### Using tmux (Linux/Mac)

```bash
tmux new-session -d -s mention_tracker 'python3 scheduler.py'
```

## Logs

- `mention_tracking.log` - Contains all scheduler and job logs
- Console output - Real-time status updates

## Stopping the Scheduler

- Press `Ctrl+C` to stop gracefully
- The scheduler will complete any running job before stopping

## Monitoring

Check if the scheduler is running:

```bash
ps aux | grep scheduler.py
```

View recent logs:

```bash
tail -f mention_tracking.log
```

