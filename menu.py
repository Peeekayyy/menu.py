import requests
import os
from datetime import datetime

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        },
        timeout=20
    )

def get_today_menu():
    url = "https://www.ssms-pilani.in/api/menu/today"
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()

def main():
    hour = datetime.now().hour
    menu = get_today_menu()

    if hour < 10:
        meal = "Breakfast"
        items = menu.get("breakfast", [])
        emoji = "🍳"
    elif hour < 16:
        meal = "Lunch"
        items = menu.get("lunch", [])
        emoji = "🍛"
    else:
        meal = "Dinner"
        items = menu.get("dinner", [])
        emoji = "🍽️"

    if not items:
        send_message(f"{emoji} *{meal}*\nMenu not updated yet.")
        return

    text = f"{emoji} *Today's {meal} (SSMS)*\n"
    text += "\n".join(f"• {item}" for item in items)

    send_message(text)

if __name__ == "__main__":
    main()
  
