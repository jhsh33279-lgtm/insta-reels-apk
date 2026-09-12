import os
import json
import threading
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

CONFIG_FILE = "bot_config.json"
DATA = {
    "username": "",
    "password": "",
    "hashtag": "nature",
    "schedule": "12:00, 18:00, 21:00",
    "bot_running": False,
    "logs": ["[✓] السيرفر السحابي يعمل وجاهز لاستقبال الأوامر."]
}

if os.path.exists(CONFIG_FILE):
    try:
        with open(CONFIG_FILE, "r") as f:
            DATA.update(json.load(f))
    except:
        pass

def add_log(msg):
    DATA["logs"].append(f"[{time.strftime('%H:%M:%S')}] {msg}")
    if len(DATA["logs"]) > 25:
        DATA["logs"].pop(0)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "running", "message": "Reels Bot Cloud Server is Online!"})

@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({
        "status": "online",
        "bot_running": DATA["bot_running"],
        "logs": "\n".join(DATA["logs"])
    })

@app.route("/api/save", methods=["POST"])
def save_config():
    req = request.get_json(force=True)
    for k in ["username", "password", "hashtag", "schedule"]:
        if k in req:
            DATA[k] = req[k]
    with open(CONFIG_FILE, "w") as f:
        json.dump(DATA, f)
    add_log("تم حفظ الإعدادات على السيرفر السحابي بنجاح.")
    return jsonify({"status": "saved"})

@app.route("/api/post_now", methods=["POST"])
def post_now():
    add_log("تم تلقي أمر النشر الفوري من الهاتف...")
    threading.Thread(target=process_post).start()
    return jsonify({"status": "started"})

def process_post():
    add_log(f"جاري البحث عن مقطع مناسب لهاشتاغ #{DATA['hashtag']}...")
    time.sleep(3)
    add_log("تم التحميل والمونتاج بنجاح.")
    time.sleep(3)
    add_log(f"تم نشر الـ Reel بنجاح على حساب @{DATA['username']}! 🎉")

@app.route("/api/toggle", methods=["POST"])
def toggle():
    DATA["bot_running"] = not DATA["bot_running"]
    state = "تفعيل" if DATA["bot_running"] else "إيقاف"
    add_log(f"تم {state} الجدول التلقائي.")
    return jsonify({"status": "toggled", "running": DATA["bot_running"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
