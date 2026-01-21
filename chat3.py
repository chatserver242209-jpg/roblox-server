import telebot
from flask import Flask, request, jsonify
import time, os, re, secrets

API_TOKEN = '8461290420:AAGjpnVwgfiRDi7ZkpwWizaIqxP1kSK_CUw'
CHAT_ID = '8334245284'
SYSTEM_KEY = secrets.token_hex(16)

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

shadow_grid = []

class NeuralBypass:
    def __init__(self):
        self.masks = ['\u200b', '\u200c', '\u200d', '\ufeff', '\u200e']
    def shredder(self, t):
        for c in self.masks: t = t.replace(c, '')
        t = re.sub(r'(.)\1+', r'\1', t)
        return re.sub(r'[^\w\s\u0600-\u06FF]', '', t).lower().strip()

nb = NeuralBypass()

@app.route('/')
def home():
    return "SYSTEM ACTIVE"

@app.route('/v1/kernel/sync', methods=['POST'])
def core_vortex():
    if request.headers.get('X-SUPER-KEY') != SYSTEM_KEY:
        return jsonify({"status": "error"}), 401
    data = request.json
    entry = {
        "id": int(time.time() * 1000),
        "user": data.get('p_name', 'Unknown'),
        "content": data.get('payload', '')
    }
    processed = nb.shredder(entry['content'])
    if any(w in processed for w in ["سب1", "سب2"]): 
        return jsonify({"status": "filtered"}), 200
    shadow_grid.append(entry)
    if len(shadow_grid) > 50: shadow_grid.pop(0)
    try:
        bot.send_message(CHAT_ID, f"USER: {entry['user']}\nMSG: {entry['content']}")
    except:
        pass
    return jsonify({"status": "synced", "grid": shadow_grid}), 200

@app.route('/v1/kernel/stream', methods=['GET'])
def pull_stream():
    if request.headers.get('X-SUPER-KEY') != SYSTEM_KEY: 
        return "", 444
    return jsonify({"stream": shadow_grid}), 200

if __name__ == '__main__':
    bot.send_message(CHAT_ID, f"SYSTEM ONLINE\nKEY: {SYSTEM_KEY}")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
