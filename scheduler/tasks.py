import time

def send_reminder(email, name):
    print(f"Sending email reminder to {name} at {email}...")
    time.sleep(2)  # Simulate network delay
    print("Reminder sent successfully!")