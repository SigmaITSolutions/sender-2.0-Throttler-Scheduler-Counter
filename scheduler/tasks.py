import time
import datetime as dt
from datetime import datetime

def send_reminder(email, name):
    print(f"Sending email reminder to {name} at {email}...")
    time.sleep(2)  # Simulate network delay
    print("Reminder sent successfully!")

def send_scheduled_derfer_mesage_to_adapter(data):
    order = data['order']
    utc_tta = datetime.utcnow().timestamp()
    tta = data['tta']
    delta =tta-utc_tta
    print(f'|order_{order}|{utc_tta}|{tta}|{delta}|')
    
    time.sleep(2) # Simulate send message to apdater
    print(f'Resend message  at {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")} START')

       