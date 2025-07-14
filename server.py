from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 从环境变量读取公众号配置
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
TO_USER_OPENID = os.getenv("TO_USER_OPENID")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")

def get_token():
    res = requests.get(
        f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APP_ID}&secret={APP_SECRET}"
    ).json()
    return res.get("access_token")

@app.route("/")
def home():
    return "✅ Calendar Server is running!"

@app.route("/push", methods=["POST"])
def push():
    data = request.json
    date = data.get("date", "")
    note = data.get("note", "")
    income = data.get("income", 0)
    cost = data.get("cost", 0)
    outdoor = "🚶" if data.get("outdoor") else "🏠"
    menstruation = "🌸" if data.get("menstruation") else ""

    access_token = get_token()
    url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"

    payload = {
        "touser": TO_USER_OPENID,
        "template_id": TEMPLATE_ID,
        "data": {
            "date": {"value": date},
            "note": {"value": note or "无"},
            "income": {"value": f"{income} 元"},
            "cost": {"value": f"{cost} 元"},
            "status": {"value": f"{outdoor} {menstruation}".strip()}
        }
    }

    res = requests.post(url, json=payload)
    return res.json()

# ✅ Zeabur 必须监听 0.0.0.0 和 PORT 环境变量
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
