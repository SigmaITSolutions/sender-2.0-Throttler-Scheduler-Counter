import time
import datetime as dt
from datetime import datetime
import asyncio
import requests
def send_reminder(email, name):
    print(f"Sending email reminder to {name} at {email}...")
    time.sleep(0.2)  # Simulate network delay
    print("Reminder sent successfully!")

async  def send_scheduled_derfer_mesage_to_adapter(data):
    order = data['order']
    utc_tta = datetime.now().timestamp()
    tta = data['tta']
    delta =utc_tta-tta
    status_code =  requests.get("https://www.bing.com/")#Simulate send package to adapter
    print(f'order_{order}|{utc_tta}|{tta}|{delta}|{status_code}|')