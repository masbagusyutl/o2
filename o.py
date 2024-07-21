import time
import json
import requests
from datetime import datetime, timedelta

# Load account data
def load_accounts(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    accounts = []
    for i in range(0, len(lines), 2):
        tg = lines[i].strip()
        hash = lines[i + 1].strip()
        accounts.append((tg, hash))
    return accounts

accounts = load_accounts('data.txt')

# Headers for the requests
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en;q=0.9,en-US;q=0.8",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json",
    "Origin": "https://oxygenminer.online",
    "Pragma": "no-cache",
    "Referer": "https://oxygenminer.online/",
    "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Microsoft Edge\";v=\"126\", \"Microsoft Edge WebView2\";v=\"126\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
}

# URLs for tasks
url_daily_reward = "https://oxygenminer.online/daily_get"
url_open_box = "https://oxygenminer.online/open_box"
url_farm = "https://oxygenminer.online/farm"
url_check_task = "https://oxygenminer.online/check_task"

# Function to perform social media tasks
def social_media_task(account):
    payload = {
        "tg": account[0],
        "hash": account[1],
        "data": "join_tw"
    }
    response = requests.post(url_check_task, headers=headers, json=payload)
    if response.status_code == 200:
        print("Social media task completed for account:", account[0])
    else:
        print("Failed to complete social media task for account:", account[0])

# Function to perform daily box opening tasks
def open_boxes(account):
    for _ in range(10):
        payload = {
            "tg": account[0],
            "hash": account[1]
        }
        response = requests.post(url_open_box, headers=headers, json=payload)
        if response.status_code == 200:
            print("Opened a box for account:", account[0])
        else:
            print("Failed to open a box for account:", account[0])
        time.sleep(1)

# Function to perform daily reward tasks
def daily_reward(account):
    payload = {
        "tg": account[0],
        "hash": account[1]
    }
    response = requests.post(url_daily_reward, headers=headers, json=payload)
    if response.status_code == 200:
        print("Daily reward claimed for account:", account[0])
    else:
        print("Failed to claim daily reward for account:", account[0])

# Function to perform farming tasks
def farm(account):
    payload = {
        "tg": account[0],
        "hash": account[1]
    }
    response = requests.post(url_farm, headers=headers, json=payload)
    if response.status_code == 200:
        print("Farming task completed for account:", account[0])
    else:
        print("Failed to complete farming task for account:", account[0])

# Function to display a moving countdown timer
def countdown_timer(duration, message):
    while duration:
        mins, secs = divmod(duration, 60)
        time_format = f"{mins:02d}:{secs:02d}"
        print(f"{message} {time_format}", end='\r')
        time.sleep(1)
        duration -= 1
    print()

# Prompt for social media tasks
def prompt_social_media():
    response = input("Do you want to complete social media tasks? (yes/no): ")
    return response.lower() == "yes"

# Main function to process all accounts
def process_accounts():
    social_media_done = False
    if prompt_social_media():
        for account in accounts:
            print(f"Processing social media task for account: {account[0]}")
            social_media_task(account)
            time.sleep(5)
        social_media_done = True

    next_daily_task = datetime.now() + timedelta(days=1)
    print("Next daily tasks scheduled for:", next_daily_task)

    while True:
        for account in accounts:
            print(f"Processing daily tasks for account: {account[0]}")
            daily_reward(account)
            open_boxes(account)
            time.sleep(5)

        while datetime.now() < next_daily_task:
            for account in accounts:
                print(f"Processing farming task for account: {account[0]}")
                farm(account)
                time.sleep(5)

            print("Waiting for the next farming task...")
            countdown_timer(3600, "Time until next farming task:")

        if datetime.now() >= next_daily_task:
            for account in accounts:
                print(f"Processing daily tasks for account: {account[0]}")
                daily_reward(account)
                open_boxes(account)
                time.sleep(5)
            next_daily_task += timedelta(days=1)
            print("Next daily tasks scheduled for:", next_daily_task)

# Run the script
process_accounts()
