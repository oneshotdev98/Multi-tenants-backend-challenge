#!/usr/bin/env python3
# Date utilities
from datetime import datetime, timedelta

def days_between(date1, date2):
    """Calculate days between two dates."""
    return abs((date2 - date1).days)

def next_weekday(date, weekday):
    """Get next occurrence of weekday."""
    days_ahead = weekday - date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return date + timedelta(days=days_ahead)
