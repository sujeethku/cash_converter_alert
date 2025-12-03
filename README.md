# Cash Converter Alert App 💰📲

A Python automation tool that checks the AUD → INR exchange rate every hour and sends a WhatsApp alert **when the rate crosses a threshold** (default: 58 INR).  
The app guarantees **only 1 alert per day**, even if the rate keeps rising.

---

## 🚀 Features

- Fetches live AUD → INR exchange rate  
- Sends real-time WhatsApp alerts using Twilio Sandbox  
- Ensures **1 alert per day** using state tracking  
- Secure `.env`-based credential management  
- Easy setup + ready for cron automation  
- Beginner-friendly, production-safe architecture  

---

## 🛠️ Tech Stack

- Python 3  
- Twilio WhatsApp Sandbox API  
- fxratesapi.com (free exchange rate API)  
- python-dotenv  
- cron (optional automation)  

---

## 📦 Setup Instructions

### 1. Clone the repo  

git clone <your-repo-url>
cd cash_converter

### 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Create .env file
TWILIO_ACCOUNT_SID=ACxxxx...
TWILIO_AUTH_TOKEN=xxxxxxxx
WHATSAPP_TO=whatsapp:+614xxxxxxx

### 🕒 Optional: Add Cron Job
0 * * * * /usr/bin/python3 /path/to/alert.py

### 📘 Architecture Summary

alert.py — main application
.env — private credentials (ignored by Git)
state.json — tracks daily alert status
requirements.txt — dependencies

### 👨‍💻 Author

Sujeeth Tuniki
AI-driven Product Manager | Python Learner | Automation Enthusiast