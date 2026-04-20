# BLOCK 1 — Imports
from apscheduler.schedulers.background import BackgroundScheduler
from functions import run_updates
import os

scheduler = BackgroundScheduler()
def refresh():
    run_updates()
    
scheduler.add_job(refresh, 'interval', minutes=60)

def start_scheduler():
    scheduler.start()