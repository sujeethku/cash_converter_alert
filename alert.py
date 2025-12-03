import requests
import datetime
import json
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()


THRESHOLD = 58
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_TO = os.getenv("WHATSAPP_TO")

STATE_FILE = "state.json"

def get_rate():
    url = "https://api.fxratesapi.com/latest?base=AUD&symbols=INR"
    response = requests.get(url)
    data = response.json()
    return data["rates"]["INR"]

def send_alert(rate):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_="whatsapp:+14155238886",   # Twilio Sandbox WhatsApp number
        body=f"🚨 AUD→INR Alert: Rate crossed {THRESHOLD}. Current rate = {rate}",
        to=WHATSAPP_TO
    )
    return message.sid

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"last_alert_date": ""}

def save_state(date):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_alert_date": date}, f)

def main():
    today = str(datetime.date.today())
    state = load_state()

    rate = get_rate()
    print("Current AUD→INR rate:", rate)

    # If threshold crossed and alert not sent today
    if rate > THRESHOLD and state["last_alert_date"] != today:
        print("Threshold crossed. Sending alert...")
        send_alert(rate)
        save_state(today)
    else:
        print("No alert needed.")

if __name__ == "__main__":
    main()
