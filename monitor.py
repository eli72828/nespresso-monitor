import os
import requests
from playwright.sync_api import sync_playwright

URL = "https://www.nespresso.com/il/he/orders/accessories/original/travel-tumbler-bubble-gum"
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def check_stock():
    with sync_playwright() as p:
        # פותחים דפדפן כרום נסתר
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # הולכים לאתר ומחכים שהרשת "תירגע" - כלומר שכל ה-JavaScript יסיים לטעון
            page.goto(URL, wait_until="networkidle")
            
            # עכשיו שולפים את ה-HTML אחרי שכל הנתונים נטענו
            html_content = page.content().lower()
            
            # בדיקת ריגול: האם אנחנו רואים עכשיו את הכוס?
            if "bubble" not in html_content:
                print("Warning: Still can't see the word 'bubble'. Nespresso might be blocking automated browsers.")
            elif "coming soon" in html_content:
                print("The cup loaded successfully! But it's still 'COMING SOON'. Checked successfully.")
            elif "הוספה לסל" in html_content:
                msg = f"☕ מהר! כוס ה-Bubble Gum זמינה עכשיו לרכישה!\nכנס ללינק: {URL}"
                send_telegram_message(msg)
                print("Alert sent to Telegram!")
            else:
                print("Something changed on the page, couldn't find 'coming soon' or 'הוספה לסל'.")
                
        except Exception as e:
            print(f"Error checking stock: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    if not BOT_TOKEN or not CHAT_ID:
        print("Missing Telegram credentials.")
    else:
        check_stock()
