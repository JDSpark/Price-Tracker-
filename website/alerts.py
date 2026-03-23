# -------------------------------------------------------
# BLOCK 1 — Imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
# -------------------------------------------------------


# -------------------------------------------------------
# BLOCK 2 — Configuration
load_dotenv()
ALERT_EMAIL_SENDER = os.getenv("ALERT_EMAIL_SENDER")
ALERT_EMAIL_PASSWORD = os.getenv("ALERT_EMAIL_PASSWORD")
ALERT_EMAIL_RECEIVER = os.getenv("ALERT_EMAIL_RECEIVER")
# -------------------------------------------------------


# -------------------------------------------------------
# BLOCK 3 — Email Builder
def build_email(product_name, old_price, new_price, url):
    msg = MIMEMultipart()
    msg["Subject"] = f"{product_name} has had a price change"
    msg["From"] = ALERT_EMAIL_SENDER
    msg["To"] = ALERT_EMAIL_RECEIVER
    msg.attach(MIMEText(f"{product_name}, {url}, has had a price change from \n{old_price} to {new_price}", "plain"))
    return msg
# -------------------------------------------------------


# -------------------------------------------------------
# BLOCK 4 — Email Sender
def send_email(msg):
    if not ALERT_EMAIL_RECEIVER:
        print("Receiving Email has not been set.")
        return
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(ALERT_EMAIL_SENDER, ALERT_EMAIL_PASSWORD)
            server.send_message(msg)
            print("Email has been sent.")
    except Exception as e:
        print(f"Error {e} ")
# -------------------------------------------------------


# -------------------------------------------------------
# BLOCK 5 — Public Interface
def send_price_alert(product_name, old_price, new_price, url):
    msg = build_email(product_name,old_price,new_price,url)
    send_email(msg)
# define send_price_alert(product_name, old_price, new_price, url)
#   this is the only function the rest of the app calls
#   call build_email() with the product info and store the result
#   call send_email() with the result
# -------------------------------------------------------