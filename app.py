from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # ✅ Active CORS pour toutes les origines

KLAVIYO_API_KEY = os.environ.get("KLAVIYO_API_KEY")

@app.route("/check-klaviyo-profile", methods=["POST"])
def check_profile():
    data = request.get_json()
    kla_id = data.get("kla_id")

    if not kla_id:
        return jsonify({"exists": False}), 400

    url = f"https://a.klaviyo.com/api/profiles/{kla_id}"
    headers = {
        "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}",
        "revision": "2023-02-22"
    }

    response = requests.get(url, headers=headers)
    return jsonify({"exists": response.ok}), 200 if response.ok else 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
