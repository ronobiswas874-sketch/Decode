from flask import Flask, request, jsonify
import base64
import json
import requests
from datetime import datetime

app = Flask(__name__)

API_URL = "https://sextyinfo.vercel.app/player-info"


def decode_segment(segment):
    padding = '=' * (-len(segment) % 4)
    return json.loads(base64.urlsafe_b64decode(segment + padding).decode('utf-8'))


def convert_time(timestamp):
    """Convert unix timestamp to readable time"""
    if not timestamp:
        return None
    return datetime.utcfromtimestamp(int(timestamp)).strftime("%d %b %Y | %I:%M %p")


def format_payload(old_payload):
    return {
        "account_id": old_payload.get("account_id"),
        "client_type": old_payload.get("client_type"),
        "client_version": old_payload.get("client_version"),
        "country_code": old_payload.get("country_code"),
        "honer_score": old_payload.get("emulator_score"),
        "exp": old_payload.get("exp"),
        "external_id": old_payload.get("external_id"),
        "external_type": old_payload.get("external_type"),
        "external_uid": old_payload.get("external_uid"),
        "is_emulator": old_payload.get("is_emulator"),
        "lock_region": old_payload.get("lock_region"),
        "lock_region_time": old_payload.get("lock_region_time"),
        "Playernickname": old_payload.get("nickname"),
        "region": old_payload.get("noti_region"),
        "plat_id": old_payload.get("plat_id"),
        "reg_avatar": old_payload.get("reg_avatar"),
        "release_channel": old_payload.get("release_channel"),
        "release_version": old_payload.get("release_version"),
        "signature_md5": old_payload.get("signature_md5"),
        "source": old_payload.get("source"),
        "using_version": old_payload.get("using_version")
    }


def get_player_info(uid):
    try:
        res = requests.get(f"{API_URL}?uid={uid}", timeout=8)

        if res.status_code != 200:
            return None

        data = res.json()

        if not data or "basicInfo" not in data:
            return None

        p  = data.get("basicInfo", {})
        pr = data.get("profileInfo", {})
        g  = data.get("clanBasicInfo", {})
        s  = data.get("socialInfo", {})   # <-- Bio এখান থেকে আসবে

        return {
            "UID": uid,
            "Likes": p.get("liked", 0),
            "Level": p.get("level"),
            "Prime Level": p.get("role"),   # <-- fixed
            "Guild UID": g.get("clanId"),
            "Guild Name": g.get("clanName"),
            "Singapore Bio": s.get("signature") or "No Bio",   # <-- fixed
            "Last Login": convert_time(p.get("lastLoginAt")),
            "Create Time": convert_time(p.get("createAt")),
            "Account Rank": p.get("rank"),
            "BR Rank": p.get("rankingPoints"),
            "CS Rank": p.get("csRankingPoints"),
            "Elite Pass": p.get("hasElitePass")
        }

    except Exception as e:
        return None


@app.route("/decode", methods=["GET"])
def decode_jwt():

    token = request.args.get("jwt")

    if not token:
        return jsonify({
            "status": "error",
            "message": "JWT token missing"
        }), 400

    try:
        header_b64, payload_b64, signature_b64 = token.split(".")

        header = decode_segment(header_b64)
        payload = decode_segment(payload_b64)

        custom_payload = format_payload(payload)

        uid = payload.get("account_id")

        player_info = get_player_info(uid)

        response = {
            "status": "success",
            "Your jwt token": token,
            "UID from JWT": uid,
            "payload": {
                **header,
                **custom_payload
            },    
            "signature": signature_b64,
            "api by": "XEROX_MOD",
            "TG": "@SEXTYMOD"
        }

        if player_info:
            response["Player Info"] = player_info

        return jsonify(response)

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


import os

if __name__ == "__main__":
    # প্যানেল থেকে পাঠানো ডাইনামিক পোর্ট রিসিভ করা
    # যদি পোর্ট না পায় তবে ডিফল্ট ৫০০০ এ চলবে (লোকাল টেস্টের জন্য)
    target_port = int(os.environ.get("PORT", 5000))
    
    # অবশ্যই host='0.0.0.0' দিতে হবে যাতে প্যানেল কানেক্ট করতে পারে
    # প্রোডাকশন বা ক্লাউড মোডে debug=False রাখা ভালো
    app.run(host='0.0.0.0', port=target_port, debug=False)
