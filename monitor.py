import os
import requests

# אל תשכח להדביק פה שוב את הלינק המדויק של נספרסו!
URL = "הכנס_כאן_את_הלינק_של_נספרסו"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, json=payload)
    print("Telegram Response:", response.text)

def check_stock():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        
        # הופכים את כל קוד האתר לאותיות קטנות כדי שלא נפספס בגלל אותיות גדולות/קטנות
        html_content = response.text.lower()
        
        # בדיקת ריגול: מה גודל העמוד והאם המילה 'bubble' בכלל נמצאת שם?
        print(f"Page size: {len(html_content)} characters")
        if "bubble" not in html_content:
            print("Warning: The word 'bubble' is not on the page. The site is hiding content from us.")
        
        # הלוגיקה המשודרגת (הכל באותיות קטנות)
        if "coming soon" in html_content:
            msg = f"☕ (הודעת ניסיון) המילה COMING SOON נמצאה בהצלחה!\n{URL}"
            send_telegram_message(msg)
            print("Alert sent to Telegram!")
        else:
            print("Still out of stock. 'coming soon' not found.")
            
    except Exception as e:
        print(f"Error checking stock: {e}")

if __name__ == "__main__":
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing Telegram credentials.")
    else:
        check_stock()
