import os
import requests

URL = "https://www.nespresso.com/il/he/orders/accessories/original/travel-tumbler-bubble-gum"
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

# הכנס כאן את שם המשתמש שלך בטלגרם (עם השטרודל) או את מספר הטלפון שלך עם 972+
CALLMEBOT_USER = "@eli_2883"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def make_telegram_call():
    # פונקציה חדשה שמתקשרת אליך ומקריאה טקסט
    params = {
        "user": CALLMEBOT_USER,
        "text": "Wake up! The Nespresso Bubble Gum cup is now in stock!",
        "lang": "en-US-Standard-B",
        "rpt": 2
    }
    try:
        requests.get("https://api.callmebot.com/start.php", params=params)
        print("Phone call initiated!")
    except Exception as e:
        print(f"Error calling: {e}")

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        
        # ה-not חזר למקומו! עכשיו הקוד סורק בשקט ומחכה למלאי האמיתי
        if "אזל זמנית" in response.text:
            msg = f"☕ חדשות מעולות! כוס ה-Bubble Gum הוורודה כנראה זמינה עכשיו!\nכנס מהר ללינק: {URL}"
            send_telegram_message(msg)
            make_telegram_call()  # הקריאה החדשה שמפעילה את שיחת הטלפון
            print("Alert sent, and phone is ringing!")
        else:
            print("Still out of stock. 'אזל זמנית' found in the page.")
            
    except Exception as e:
        print(f"Error checking stock: {e}")

if __name__ == "__main__":
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing Telegram credentials.")
    else:
        check_stock()
