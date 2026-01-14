import time
from datetime import datetime
def send_reminder(email, name):
    print(f"Sending email reminder to {name} at {email}...")
    time.sleep(2)  # Simulate network delay
    print("Reminder sent successfully!")

def send_scheduled_derfer_mesage_to_adapter(data):
    print(f'Resend message  at {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")} START')
    time.sleep(2) # Simulate send message to apdater
    print(f'Resend message  at {datetime.now().strftime("%d/%m/%Y, %H:%M:%S")} START')

       