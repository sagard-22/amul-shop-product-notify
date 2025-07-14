import os
import sys
import time
import random
import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === Configuration ===

# Colab secrets
# from google.colab import userdata
# sender_email = userdata.get('SENDER_EMAIL')
# receiver_email = userdata.get('RECEIVER_EMAIL')
# email_password = userdata.get('SENDER_PASSWORD')
    
# env vars
sender_email = os.getenv('SENDER_EMAIL')
receiver_email = os.getenv('RECEIVER_EMAIL')
email_password = os.getenv('SENDER_PASSWORD')

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

PRODUCT_URLS = [
    #"https://shop.amul.com/en/product/amul-high-protein-rose-lassi-200-ml-or-pack-of-30",
    "https://shop.amul.com/en/product/amul-chocolate-whey-protein-gift-pack-34-g-or-pack-of-10-sachets",
    "https://shop.amul.com/en/product/amul-chocolate-whey-protein-34-g-or-pack-of-30-sachets",
    "http://shop.amul.com/en/product/amul-chocolate-whey-protein-34-g-or-pack-of-60-sachets",
    #"https://shop.amul.com/en/product/amul-high-protein-plain-lassi-200-ml-or-pack-of-30",
    #"https://shop.amul.com/en/product/amul-high-protein-buttermilk-200-ml-or-pack-of-30",
    #"https://shop.amul.com/en/product/amul-whey-protein-gift-pack-32-g-or-pack-of-10-sachets",
    #"https://shop.amul.com/en/product/amul-whey-protein-32-g-or-pack-of-30-sachets",
]

#Your location
STORE = "mumbai-br"

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Origin": "https://shop.amul.com",
    "Referer": "https://shop.amul.com/",
    "base_url": PRODUCT_URLS[0],
    "frontend": "1",
    "tid": f"{int(time.time() * 1000)}:{random.randint(100, 999)}:{''.join(random.choices('abcdef0123456789', k=64))}"
}


session = requests.Session()

# Extract product aliases
PRODUCT_ALIASES = [url.rstrip('/').split('/')[-1] for url in PRODUCT_URLS]


def set_preferences(store: str) -> bool:
    """Set store preferences on the website."""
    url = "https://shop.amul.com/entity/ms.settings/_/setPreferences"
    payload = {"data": {"store": store}}
    response = session.put(url, headers=HEADERS, data=json.dumps(payload))
    if response.ok:
        print("[INFO] Preferences set successfully.")
        return True
    print(f"[ERROR] Failed to set preferences. Status code: {response.status_code}")
    return False


def is_product_available(product_alias: str) -> bool:
    """Check if a product is available."""
    url = "https://shop.amul.com/api/1/entity/ms.products"
    params = {
        "q": json.dumps({"alias": product_alias}),
        "limit": 1,
    }
    response = session.get(url, headers=HEADERS, params=params)
    if response.ok:
        data = response.json()
        if data.get('data'):
            return data['data'][0].get('available', 0) > 0
    return False


def send_email(product_name: str) -> None:
    """Send email notification."""
    if not all([sender_email, receiver_email, email_password]):
        raise ValueError("[ERROR] Email credentials are not set.")

    subject = f"Product Available: {product_name}"
    body = f"The product '{product_name}' is now available on Amul's website."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, email_password)
            server.send_message(msg)
        print(f"[INFO] Email sent to {receiver_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")


def check_products_and_notify() -> None:
    """Main workflow to check products and notify if available."""
    # Step 1: Trigger session cookies via API call
    session.get("https://shop.amul.com/api/1/entity/ms.homepage", headers=HEADERS)

    if not set_preferences(STORE):
        print("[FATAL] Exiting due to preference setting failure.")
        sys.exit(1) 
        return

    for product_alias in PRODUCT_ALIASES:
        print(f"[INFO] Checking availability for '{product_alias}'...")
        if is_product_available(product_alias):
            print(f"[ALERT] '{product_alias}' is available!")
            send_email(product_alias)
        else:
            print(f"[INFO] '{product_alias}' is not available.")



check_products_and_notify()
