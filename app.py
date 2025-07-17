from flask import Flask, jsonify
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def get_youtube_cookies():
    try:
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Use existing user profile if you want persistent login
        # options.add_argument("--user-data-dir=/home/youruser/.config/google-chrome")

        driver = uc.Chrome(options=options)
        driver.get("https://youtube.com")

        print("Waiting for YouTube to load...")
        time.sleep(10)  # Give time to manually login if needed

        cookies = driver.get_cookies()
        driver.quit()

        cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        return cookie_dict

    except Exception as e:
        return {"error": str(e)}

@app.route('/cookies')
def cookies():
    return jsonify(get_youtube_cookies())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
