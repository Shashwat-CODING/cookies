from flask import Flask, jsonify
import browser_cookie3
import json

app = Flask(__name__)

@app.route("/cookies")
def get_youtube_cookies():
    try:
        # Load Chrome cookies only for YouTube domain
        cj = browser_cookie3.chrome(domain_name="youtube.com")

        cookies = []
        for c in cj:
            cookies.append({
                "name": c.name,
                "value": c.value,
                "domain": c.domain,
                "path": c.path,
                "secure": c.secure,
                "expires": c.expires
            })

        return jsonify({"cookies": cookies})

    except Exception as e:
        return jsonify({"error": f"Failed to load cookies: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
