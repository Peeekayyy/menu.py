import requests
import os
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.ssms-pilani.in/"

def get_today_menu():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(URL, headers=headers)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    # This may need small tweaks if site changes
    menu_sections = soup.find_all("div", class_="card")

    text = "🍽️ *SSMS Menu Today*\n\n"
    for section in menu_sections:
        title = section.find("h5")
        body = section.find("p")
        if title and body:
            text += f"*{title.text.strip()}*\n{body.text.strip()}\n\n"

    return text.strip()

def send_telegram(msg):
    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    requests.post(api, json=payload)

def main():
    menu = get_today_menu()
    send_telegram(menu)

if __name__ == "__main__":
    main()
    
