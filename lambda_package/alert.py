import boto3
import requests
import datetime
import json
from twilio.rest import Client
import os

# S3 config
s3 = boto3.client("s3")
BUCKET_NAME = "cash-converter-alert-state-st"
STATE_FILE_KEY = "state.json"

# Load Twilio credentials from AWS Secrets Manager
def get_twilio_credentials():
    secrets_client = boto3.client("secretsmanager")

    secret_name = os.environ["TWILIO_SECRET_NAME"]  # we set this soon

    response = secrets_client.get_secret_value(SecretId=secret_name)

    secrets = json.loads(response["SecretString"])

    return secrets["TWILIO_ACCOUNT_SID"], secrets["TWILIO_AUTH_TOKEN"]


THRESHOLD = 58
TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN = get_twilio_credentials()
WHATSAPP_TO = os.environ["WHATSAPP_TO"] # MUST COME FROM LAMBDA ENV VAR

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
        response = s3.get_object(Bucket=BUCKET_NAME, Key=STATE_FILE_KEY)
        content = response["Body"].read().decode("utf-8")
        return json.loads(content)
    except s3.exceptions.NoSuchKey:
        # File doesn't exist yet — return default state
        return {"last_alert_date": None}
    except Exception as e:
        print("Error loading state:", e)
        return {"last_alert_date": None}

def save_state(state):
    try:
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=STATE_FILE_KEY,
            Body=json.dumps(state)
        )
    except Exception as e:
        print("Error saving state:", e)

def main(event=None, context=None):
    today = str(datetime.date.today())
    state = load_state()

    rate = get_rate()
    print("Current AUD→INR rate:", rate)

    # If threshold crossed and alert not sent today
    if rate > THRESHOLD and state["last_alert_date"] != today:
        print("Threshold crossed. Sending alert...")
        send_alert(rate)
        save_state({"last_alert_date": today})

    else:
        print("No alert needed.")

if __name__ == "__main__":
    main()
