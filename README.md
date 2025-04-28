# 🛒 Amul Shop Product Availability Notifier

This repository contains a simple Python script that checks if selected products on the [Amul Shop](https://shop.amul.com) website are available and **sends an email notification** when they are!

The checking is **automated** using **GitHub Actions** to run every few minutes.

---

## 📋 Features
- Check availability for selected Amul products.
- Send an email when a product becomes available.
- Fully automated — runs every 10 minutes (or your custom interval) using GitHub Actions.
- Easy to configure your own email, products, and store location.

---

## 🚀 Quick Setup

### 1. Fork this repository

Click on the top-right "Fork" button in GitHub and create your own copy.

---

### 2. Set up GitHub Repository Secrets

You need to add **3 secrets** in your GitHub repository settings:

Go to:  
➡️ `Settings > Secrets and Variables > Actions > New repository secret`

Add the following secrets:

| Secret Name      | Description                               |
|------------------|-------------------------------------------|
| `SENDER_EMAIL`    | Your email address (used to send email)    |
| `SENDER_PASSWORD` | Your email account app password (not your real password! See below) |
| `RECEIVER_EMAIL`  | The email address to receive notifications |

**Important:**  
If you are using Gmail, create an **App Password** (not your regular password).  
You can generate it from your Google Account → Security → App Passwords.  
[Learn how to create an App Password](https://support.google.com/accounts/answer/185833)

---

### 3. Customize Products to Track

Edit `app.py` and modify the `PRODUCT_URLS` list to track your favorite products:

```python
PRODUCT_URLS = [
    "https://shop.amul.com/en/product/amul-kool-protein-milkshake-or-chocolate-180-ml-or-pack-of-30",
    "https://shop.amul.com/en/product/amul-chocolate-whey-protein-34-g-or-pack-of-60-sachets",
    # Add more product URLs here
]
```

Make sure you copy the correct product URLs directly from [shop.amul.com](https://shop.amul.com).

---

### 4. Change Your Store Location

The script defaults to `"telangana"` store.  
To change it, edit the `STORE` variable in `app.py`:

```python
STORE = "your-location-here"  # Example: "pune-br". Go to amul shop in browser and enter pincode to see your city/state code.
```

Use lowercase names and match exactly as used by Amul website.

---

### 5. Customize the Checking Frequency (Optional)

By default, the GitHub Action checks every **10 minutes**.

If you want to change it, edit the cron schedule in `.github/workflows/app.yml`:

```yaml
on:
  schedule:
    - cron: "*/10 * * * *"  # Every 10 minutes
```

Here are some examples:

| Cron Expression | Meaning                      |
|-----------------|-------------------------------|
| `*/5 * * * *`    | Every 5 minutes               |
| `0 * * * *`      | Every hour at minute 0        |
| `0 9 * * *`      | Every day at 9:00 AM UTC       |

You can generate custom cron timings here: [crontab.guru](https://crontab.guru/).

---

## ⚡ Important Note About GitHub Action Minutes

GitHub provides limited **free minutes** per month.

- Once you receive the product notification and no longer need alerts,  
  **please remember to disable or delete the GitHub Action workflow**.
  
This helps you **save GitHub Actions minutes** and avoid unnecessary usage.

To disable:
- Go to **Actions → Your Workflow → Disable Workflow** (button on GitHub).

---

## 🛠 How It Works

- **Step 1:** Sets your store location on Amul website.
- **Step 2:** Checks if the listed products are available.
- **Step 3:** If available, sends you an email notification.
- **Step 4:** Runs automatically every X minutes via GitHub Actions!

---

## 📎 Notes
- This project is for educational/personal use only.

---
