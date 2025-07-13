import os
import json
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Cổng động cho Render hoặc Railway
PORT = int(os.environ.get("PORT", 5000))

# Cấu hình mặc định (bạn cần thay đổi nếu có client_id thật)
GARENA_ENDPOINT = "https://100067.connect.garena.com/api/v2/oauth/guest:register"
CLIENT_ID = "abc123"  # <-- Thay client_id của bạn vào đây

def generate_device_id():
    import uuid
    return str(uuid.uuid4())

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "API Garena Guest Register đang hoạt động 🟢",
        "usage": "/register để tạo tài khoản guest"
    })

@app.route("/register", methods=["POST"])
def register_guest():
    try:
        device_id = generate_device_id()

        payload = {
            "client_id": CLIENT_ID,
            "platform": "guest",
            "device_id": device_id
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(GARENA_ENDPOINT, json=payload, headers=headers)
        data = response.json()

        if "user_id" in data:
            return jsonify({
                "status": "success",
                "user_id": data["user_id"],
                "access_token": data.get("access_token"),
                "guest": data.get("guest", True)
            })
        else:
            return jsonify({
                "status": "error",
                "details": data
            }), 400

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
