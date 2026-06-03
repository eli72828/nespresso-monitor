import os
import requests

# כאן צריך להדביק את הלינק המדויק לעמוד המוצר של הכוס
URL = "https://www.nespresso.com/il/he/orders/accessories/original/travel-tumbler-bubble-gum"

# משיכת הנתונים ממשתני הסביבה (נגדיר אותם ב-GitHub בהמשך)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)


def check_stock():
    # הוספת User-Agent כדי שהאתר לא יחשוב שאנחנו בוט חסימה
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()

        # הלוגיקה: אם "COMING SOON" לא נמצא בטקסט או ש"הוספה לסל" מופיע
        if "COMING SOON" not in response.text or "הוספה לסל" in response.text:
            msg = f"☕ חדשות טובות! כוס ה-Bubble Gum זמינה כנראה לרכישה עכשיו!\nכנס מהר: {URL}"
            send_telegram_message(msg)
            print("Alert sent to Telegram!")
        else:
            print("Still out of stock. Checked successfully.")

    except Exception as e:
        print(f"Error checking stock: {e}")


if __name__ == "__main__":
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing Telegram credentials.")
    else:
        check_stock()