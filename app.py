from flask import Flask, jsonify
import browser_cookie3
import undetected_chromedriver as uc
import time
import threading
import datetime

app = Flask(__name__)

YOUTUBE_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # safe video for loading cookies

def play_youtube_to_refresh_cookies():
    try:
        options = uc.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--mute-audio")
        options.add_argument("--disable-extensions")

        driver = uc.Chrome(options=options)
        driver.get(YOUTUBE_URL)

        time.sleep(10)  # Let cookies get refreshed

        driver.quit()
        print("✅ Refreshed YouTube cookies.")
    except Exception as e:
        print(f"❌ Failed to refresh YouTube cookies: {e}")


def convert_cookie(cookie):
    return {
        "domain": cookie.domain,
        "expirationDate": float(cookie.expires) if cookie.expires else None,
        "hostOnly": not cookie.domain.startswith("."),
        "httpOnly": cookie._rest.get("httpOnly", False),
        "name": cookie.name,
        "path": cookie.path,
        "sameSite": "no_restriction",
        "secure": cookie.secure,
        "session": False if cookie.expires else True,
        "storeId": "0",
        "value": cookie.value
    }

@app.route("/cookies")
def get_youtube_cookies():
    # Step 1: Launch Chrome & play video in background (threaded)
    thread = threading.Thread(target=play_youtube_to_refresh_cookies)
    thread.start()
    thread.join()

    # Step 2: Extract cookies using browser_cookie3 (Chrome only)
    try:
        cj = browser_cookie3.chrome()
    except Exception as e:
        return jsonify({"error": f"Failed to load cookies: {str(e)}"}), 500

    # Step 3: Filter YouTube cookies and format
    cookies = []
    for cookie in cj:
        if "youtube.com" in cookie.domain:
            cookies.append(convert_cookie(cookie))

    return jsonify(cookies)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

